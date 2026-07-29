"""Overall decision confidence: how much do we trust the data we based
this decision on? Confidence is low when analyzers returned little or
low-confidence data (e.g. a brand-new agent, an unrecognized token, no
simulation backend configured) — a decision can be directionally correct
but should still say plainly "we weren't sure".
"""
from __future__ import annotations

from typing import List

from guardian.core.models import Signal


def compute_confidence(signals: List[Signal]) -> float:
    scored = [s for s in signals if s.confidence > 0]
    if not scored:
        return 0.3  # a decision was made essentially blind

    avg = sum(s.confidence for s in scored) / len(scored)
    # Small reward for having multiple independent sources weigh in.
    coverage_bonus = min(0.1, 0.02 * len({s.source for s in scored}))
    return max(0.0, min(1.0, avg + coverage_bonus))
