"""Agent Reputation Engine.

Tracks how an agent's past decisions should influence trust in its future
requests. Reputation starts at a neutral prior for unknown agents and
moves based on the outcome history stored in memory: ALLOW nudges it up,
WARN nudges it down more, BLOCK nudges it down sharply.
"""
from __future__ import annotations

from guardian.core.models import DecisionType
from guardian.memory.history import DecisionHistory

NEUTRAL_SCORE = 50.0
MIN_SCORE = 0.0
MAX_SCORE = 100.0

DELTA = {
    DecisionType.ALLOW: +2.0,
    DecisionType.WARN: -5.0,
    DecisionType.BLOCK: -15.0,
}


class AgentReputation:
    def __init__(self, history: DecisionHistory):
        self.history = history

    def score_for(self, agent_id: str) -> float:
        records = self.history.get(agent_id)
        if not records:
            return NEUTRAL_SCORE

        score = NEUTRAL_SCORE
        for record in records:
            score += DELTA.get(record.decision, 0.0)
        return max(MIN_SCORE, min(MAX_SCORE, score))

    def history_size(self, agent_id: str) -> int:
        return len(self.history.get(agent_id))
