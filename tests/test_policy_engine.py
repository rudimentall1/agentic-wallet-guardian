import unittest

from guardian.core.context import EvaluationContext
from guardian.core.intent import ActionIntent
from guardian.policy.engine import PolicyEngine


class TestPolicyEngine(unittest.TestCase):
    def test_blocked_action_type(self):
        policy = {
            "blocked_action_types": ["self_destruct"],
            "max_amount_per_action": 100,
            "max_amount_unknown_agent": 10,
            "high_value_threshold": 50,
            "min_reputation_for_high_value": 60,
            "require_confirmation_action_types": [],
        }
        engine = PolicyEngine(policy)
        intent = ActionIntent(agent_id="a", wallet="0x1", action_type="self_destruct", amount=1)
        ctx = EvaluationContext(intent=intent, agent_reputation_score=50, agent_history_size=1)
        violations = engine.evaluate(ctx)
        self.assertTrue(any(v.rule == "blocked_action_type" for v in violations))

    def test_high_value_low_reputation_is_flagged(self):
        engine = PolicyEngine()
        intent = ActionIntent(agent_id="a", wallet="0x1", action_type="swap", amount=1000)
        ctx = EvaluationContext(intent=intent, agent_reputation_score=10, agent_history_size=5)
        violations = engine.evaluate(ctx)
        rules = {v.rule for v in violations}
        self.assertTrue({"amount_exceeds_cap", "reputation_too_low_for_value"} & rules)

    def test_within_caps_produces_no_violations(self):
        engine = PolicyEngine()
        intent = ActionIntent(agent_id="a", wallet="0x1", action_type="swap", amount=1)
        ctx = EvaluationContext(intent=intent, agent_reputation_score=80, agent_history_size=10)
        violations = engine.evaluate(ctx)
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
