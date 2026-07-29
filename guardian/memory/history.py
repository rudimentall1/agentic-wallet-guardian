"""Decision history: append-only record of past Guardian decisions per
agent, used both for Agent Reputation and for building context ("this
agent has done N swaps before, this is not new behavior").
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from guardian.core.models import Decision, DecisionType
from guardian.memory.storage import InMemoryStorage, MemoryBackend


@dataclass
class HistoryRecord:
    intent_id: str
    decision: DecisionType
    risk_score: float
    created_at: float


class DecisionHistory:
    def __init__(self, backend: Optional[MemoryBackend] = None):
        self.backend = backend or InMemoryStorage()

    def record(self, agent_id: str, decision: Decision) -> None:
        self.backend.append(agent_id, {
            "intent_id": decision.intent_id,
            "decision": decision.decision.value,
            "risk_score": decision.risk_score,
            "created_at": decision.created_at,
        })

    def get(self, agent_id: str) -> List[HistoryRecord]:
        raw = self.backend.get(agent_id)
        return [
            HistoryRecord(
                intent_id=r["intent_id"],
                decision=DecisionType(r["decision"]),
                risk_score=r["risk_score"],
                created_at=r["created_at"],
            )
            for r in raw
        ]
