"""Assembles the full evaluation context for an intent: signals gathered
from every intelligence source, plus reputation and history lookups. This
is the object passed into the policy engine, the risk fusion engine and
the explanation builder — it is the single shared state of one evaluation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from guardian.core.intent import ActionIntent
from guardian.core.models import Signal


@dataclass
class EvaluationContext:
    intent: ActionIntent
    signals: List[Signal] = field(default_factory=list)
    agent_reputation_score: float = 50.0  # neutral prior for a brand-new agent
    agent_history_size: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)

    def add_signal(self, signal: Signal) -> None:
        self.signals.append(signal)

    def signals_from(self, source: str) -> List[Signal]:
        return [s for s in self.signals if s.source == source]
