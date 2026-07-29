# Agentic Wallet Guardian v3

**Decision infrastructure for autonomous AI agents.**
The service every autonomous AI agent consults *before* executing a blockchain action.

```
POST /decision   ->   ALLOW / WARN / BLOCK  (with a reasoned explanation)
```

---

## What changed from v2

v2 was a **wallet scanner**: you gave it an address, it gave you a score.

v3 is **decision infrastructure**: the unit of analysis is no longer a wallet,
it's an **action an agent is about to take**.

```
v2:  analyze(wallet)              -> risk_score
v3:  evaluate(action_intent)      -> decision + evidence + reasoning
```

And the reasoning is explicit, not just a number:

```
v2:  "risk 70 because balance is small"

v3:  "this action targets a new, unverified contract; the agent has no
      prior history with this kind of operation; policy requires
      confirmation for actions above 25 units from an agent at this
      reputation level."
```

v3 keeps everything from v2 that was actually a real idea (risk fusion,
explainable decisions, agent reputation, policy engine, security memory)
and drops everything that was hackathon scaffolding (the FastAPI monolith
tied to a single wallet-scanning code path, demo-only structure, and —
bluntly — the empty `Dockerfile`/`requirements.txt`/`docker-compose.yml`
that shipped in v2's repo). Every file in *this* repo has real content and
the project actually builds and runs.

---

## Architecture

```
                AI Agent
                    |
                    v
             Action Intent
   { agent_id, wallet, chain, action_type,
     target, amount, metadata }
                    |
                    v
        ┌─────────────────────────┐
        │   Guardian Decision      │
        │        Engine             │
        ├───────────────────────────┤
        │  1. Hard Rules             │  <- chain support, sanity checks
        │  2. Wallet Intelligence     │
        │  3. Token Intelligence       │
        │  4. Contract Intelligence     │
        │  5. Simulation                 │  <- pre-execution dry-run (pluggable)
        │  6. Threat Intelligence          │
        │  7. Policy Engine                 │  <- spending caps, reputation gates
        │  8. Risk Fusion                    │  <- signals -> single 0-100 score
        │  9. Reputation Adjustment            │
        │ 10. Explanation                       │  <- evidence -> human-readable reasons
        └───────────────────────────────────────┘
                    |
                    v
          ALLOW / WARN / BLOCK
                    |
                    v
          Blockchain Execution
```

### Repository layout

```
guardian/
    core/            ActionIntent, Signal, Decision, EvaluationContext
                         (zero external dependencies — no pydantic/FastAPI)
    decision/        DecisionEngine (orchestrator), RiskFusionEngine, hard rules
    reasoning/        explanation + confidence builders
    intelligence/
        wallet/        wallet reputation/age/activity signals
        token/          liquidity / asset-recognition signals
        contract/        verification / upgradeability signals
        simulation/       pre-execution dry-run (pluggable, stubbed by default)
        threat/            sanctions / threat-intel lookups
    policy/           PolicyEngine + policy templates (spending caps, reputation gates)
    reputation/       AgentReputation (score derived from decision history)
    memory/           pluggable storage backend + DecisionHistory
api/
    main.py           FastAPI app: /decision, /health, /capabilities, /agents/{id}/history, /demo/{scenario}
    schemas.py        pydantic request/response models (API boundary only)
tests/                unit tests for the engine, policy engine and reputation
```

`guardian/*` is intentionally dependency-free (standard library only), so
the decision core can be unit-tested, embedded in another service, or
ported to a different web framework without dragging FastAPI along. Only
`api/` touches pydantic/FastAPI.

---

## Honesty about the current state

This is a real, runnable, tested decision **architecture** — not yet a
production risk product. Specifically:

- **Wallet / token / contract analyzers currently return deterministic
  mock data**, clearly marked `TODO(production)` in each file. They exist
  to prove the pipeline shape (signal → fusion → policy → decision →
  explanation) end to end, not to make real risk claims about a real
  address yet.
- **Simulation is a stub.** Wiring up a real pre-execution dry-run
  (a forked-node `eth_call`, Tenderly, etc.) is the single highest-value
  next step — it's the difference between "looks statistically risky" and
  "we know exactly what this transaction would do."
- **Threat intelligence and the contract allow/deny lists are empty
  sets.** They need a real feed (OFAC SDN, Chainalysis/TRM, GoPlus,
  community scam-address lists) before a `BLOCK` from this source means
  anything.
- **Memory is in-process only** (`InMemoryStorage`). Fine for a single
  instance / demo; swap in a Redis or Postgres backend (implement the
  `MemoryBackend` protocol in `guardian/memory/storage.py`) before running
  more than one replica.

Everything downstream of a `Signal` — fusion, policy, reputation,
explanation, the API — does **not** need to change when any of the above
get replaced with real integrations. That boundary is the actual design
contract of v3.

---

## Quickstart

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Or with Docker:

```bash
docker compose up --build
```

Try the canned scenarios (mirrors the old README's SAFE / UNKNOWN / MALICIOUS demo):

```bash
curl http://localhost:8000/demo/safe
curl http://localhost:8000/demo/unknown
curl http://localhost:8000/demo/malicious
```

Or submit your own intent:

```bash
curl -X POST http://localhost:8000/decision \
  -H "Content-Type: application/json" \
  -d '{
        "agent_id": "trading-agent-001",
        "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "chain": "ethereum",
        "action_type": "swap",
        "from_token": "ETH",
        "to_token": "USDC",
        "amount": 5
      }'
```

Example response:

```json
{
  "decision": "ALLOW",
  "risk_score": 3.37,
  "risk_level": "LOW",
  "confidence": 0.92,
  "explanation": [
    "Wallet has an established history (490 days, 343 txs)",
    "USDC is a widely-held, liquid asset"
  ],
  "signals": [ ... ],
  "policy_violations": [],
  "agent_id": "trading-agent-001",
  "intent_id": "..."
}
```

---

## Running the tests

```bash
pip install -r requirements.txt
pytest -q
```

The `guardian/*` core has no external dependencies, so its tests also run
with nothing installed beyond the standard library:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

---

## Roadmap to a real product

1. Replace the mock wallet/token/contract analyzers with real data sources
   (Etherscan/Blockscout, GoPlus Security API, on-chain LP queries).
2. Wire up real pre-execution simulation.
3. Populate threat-intel / sanctions feeds; stop shipping empty sets.
4. Swap `InMemoryStorage` for a persistent backend for anything beyond a
   single-instance demo.
5. Add an MCP server wrapper and an SDK (Python/TypeScript) so agent
   frameworks (LangChain, CrewAI, custom MCP agents) can call Guardian as
   a tool without hand-rolling HTTP calls.
6. Publish an OpenAPI spec and a hosted demo endpoint.
7. Get the policy engine and risk fusion reviewed/audited before anyone
   relies on a `BLOCK` from this service in production — it's a security
   tool, so it needs the same scrutiny it applies to others.
