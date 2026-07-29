"""Builds a human-readable explanation from evidence, instead of just a
number. This is the core difference the v3 architecture is built around:
the consumer of a decision (a human reviewing an agent's action, or a
downstream system) sees *why*, not just a score.

    v2: "risk 70 because balance is small"
    v3: "this action requires interacting with a new contract that shows
         elevated-risk indicators; the agent has no prior history with
         this kind of operation, so confirmation is required."
"""
from __future__ import annotations

from typing import List

from guardian.core.models import PolicyViolation, Signal


def build_explanation(signals: List[Signal], violations: List[PolicyViolation]) -> List[str]:
    lines: List[str] = []

    # Policy violations are the most actionable, explicit reasons — lead with them.
    for v in violations:
        lines.append(f"[{v.severity}] {v.message}")

    # Then the most significant signals, ranked by score * confidence,
    # skipping zero-confidence placeholders (e.g. an unconfigured simulator).
    meaningful = [s for s in signals if s.confidence > 0 and s.reason]
    meaningful.sort(key=lambda s: s.score * s.confidence, reverse=True)

    for s in meaningful[:6]:
        lines.append(s.reason)

    if not lines:
        lines.append(
            "No risk indicators detected across wallet, token, contract and threat-intel checks"
        )

    return lines
