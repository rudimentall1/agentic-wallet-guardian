"""Policy Engine: evaluates business/risk-appetite rules that are
independent of the statistical risk score — spending caps, reputation
gates, action-type restrictions. This is where an operator encodes "what
we as an organization are willing to let an agent do", as distinct from
"how dangerous does this specific action look" (that's risk fusion).
"""
from __future__ import annotations

from typing import Dict, List, Optional

from guardian.core.context import EvaluationContext
from guardian.core.models import PolicyViolation
from guardian.policy.templates import DEFAULT_POLICY


class PolicyEngine:
    def __init__(self, policy: Optional[Dict] = None):
        self.policy = policy or DEFAULT_POLICY

    def evaluate(self, ctx: EvaluationContext) -> List[PolicyViolation]:
        intent = ctx.intent
        violations: List[PolicyViolation] = []

        if intent.action_type in self.policy.get("blocked_action_types", []):
            violations.append(PolicyViolation(
                rule="blocked_action_type",
                message=f"Action type '{intent.action_type}' is blocked by policy",
                severity="BLOCK",
            ))

        amount = intent.amount or 0.0
        is_unknown_agent = ctx.agent_history_size == 0
        cap = (
            self.policy.get("max_amount_unknown_agent")
            if is_unknown_agent
            else self.policy.get("max_amount_per_action")
        )
        if cap is not None and amount > cap:
            violations.append(PolicyViolation(
                rule="amount_exceeds_cap",
                message=f"Amount {amount} exceeds policy cap {cap} for this agent",
                severity="BLOCK" if is_unknown_agent else "WARN",
            ))

        high_value_threshold = self.policy.get("high_value_threshold")
        min_rep = self.policy.get("min_reputation_for_high_value")
        if high_value_threshold is not None and amount > high_value_threshold:
            if ctx.agent_reputation_score < (min_rep or 0):
                violations.append(PolicyViolation(
                    rule="reputation_too_low_for_value",
                    message=(
                        f"Action value {amount} requires reputation >= {min_rep}, "
                        f"agent currently has {ctx.agent_reputation_score:.0f}"
                    ),
                    severity="WARN",
                ))

        if intent.action_type in self.policy.get("require_confirmation_action_types", []):
            violations.append(PolicyViolation(
                rule="requires_confirmation",
                message=f"Action type '{intent.action_type}' always requires human confirmation",
                severity="WARN",
            ))

        return violations
