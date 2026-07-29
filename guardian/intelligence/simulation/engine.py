"""Pre-execution transaction simulation.

In production this should dry-run the intent (e.g. an ``eth_call`` against
a forked node, a Tenderly-style simulation, or a local fork) to catch
reverts, unexpected token transfers, or balance-draining side effects
*before* Guardian returns a decision. Here it is a structural placeholder
that keeps the pipeline shape correct — a real simulator can be dropped in
later without touching the decision engine, scoring, or policy layer.
"""
from __future__ import annotations

from typing import List

from guardian.core.intent import ActionIntent
from guardian.core.models import Signal


class SimulationEngine:
    source = "simulation"

    def simulate(self, intent: ActionIntent) -> List[Signal]:
        # TODO(production): run a real simulation and turn reverts, unexpected
        # token transfers, or unlimited approvals into high-risk Signals here.
        if intent.action_type == "approve" and (intent.amount is None or intent.amount <= 0):
            return [Signal(
                source=self.source, name="unlimited_approval", score=65, weight=1.5,
                confidence=0.7,
                reason="Approval has no explicit finite amount — may grant unlimited spending",
            )]
        return [Signal(
            source=self.source, name="simulation_not_configured", score=0, weight=0.0,
            confidence=0.0, reason="No simulation backend configured — skipped",
        )]
