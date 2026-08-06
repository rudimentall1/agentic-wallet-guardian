# Agentic Wallet Guardian

Self-hosted decision engine for evaluating blockchain actions before an AI agent signs or broadcasts them.

## Problem

Autonomous agents can interact with wallets, tokens, and contracts at machine speed. A useful security layer needs to evaluate the intended action, apply policy, combine intelligence signals, and return an explainable decision before execution.

## Solution

Guardian exposes a decision pipeline that returns:

`ALLOW / WARN / BLOCK`

with evidence and human-readable reasoning.

## Architecture

```text
AI Agent
   |
   v
Action Intent
   |
   +--> Hard Rules
   +--> Wallet Intelligence
   +--> Token Intelligence
   +--> Contract Intelligence
   +--> Simulation
   +--> Threat Intelligence
   +--> Policy Engine
   +--> Risk Fusion
   +--> Agent Reputation
   |
   v
Explainable Decision
   |
   v
ALLOW / WARN / BLOCK
```

## Design

The decision core is separated from the HTTP API. Intelligence providers expose replaceable interfaces so mock data can be used for development while real RPC, token, contract, and threat-intelligence sources can be introduced independently.

The repository also includes an MCP interface for agent frameworks that support MCP.

## Stack

- Python
- FastAPI
- Pydantic
- Web3.py
- Docker
- MCP
- SQLite / in-memory storage

## Quickstart

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Or:

```bash
docker compose up --build
```

## Tests

```bash
pytest -q
```

The repository contains tests for the decision engine, policy, reputation, and provider layers.

## Current State

Runnable security decision infrastructure with real provider integrations available for wallet, token, and contract intelligence. Pre-execution simulation remains an important area for further hardening, and the project has not been independently security-audited.

## Status

Active engineering project / security infrastructure prototype.
