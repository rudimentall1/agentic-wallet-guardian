import unittest

from guardian.core.models import Decision, DecisionType, RiskLevel
from guardian.memory.history import DecisionHistory
from guardian.reputation.agent import NEUTRAL_SCORE, AgentReputation


def _fake_decision(agent_id: str, decision_type: DecisionType) -> Decision:
    return Decision(
        decision=decision_type, risk_score=0, risk_level=RiskLevel.LOW, confidence=1.0,
        explanation=[], signals=[], policy_violations=[], agent_id=agent_id, intent_id="x",
    )


class TestReputation(unittest.TestCase):
    def test_neutral_for_unknown_agent(self):
        rep = AgentReputation(DecisionHistory())
        self.assertEqual(rep.score_for("nobody"), NEUTRAL_SCORE)

    def test_score_drops_after_blocks(self):
        history = DecisionHistory()
        rep = AgentReputation(history)
        history.record("bad-agent", _fake_decision("bad-agent", DecisionType.BLOCK))
        history.record("bad-agent", _fake_decision("bad-agent", DecisionType.BLOCK))
        self.assertLess(rep.score_for("bad-agent"), NEUTRAL_SCORE)

    def test_score_rises_after_allows(self):
        history = DecisionHistory()
        rep = AgentReputation(history)
        for _ in range(10):
            history.record("good-agent", _fake_decision("good-agent", DecisionType.ALLOW))
        self.assertGreater(rep.score_for("good-agent"), NEUTRAL_SCORE)

    def test_score_is_clamped_between_0_and_100(self):
        history = DecisionHistory()
        rep = AgentReputation(history)
        for _ in range(50):
            history.record("very-bad-agent", _fake_decision("very-bad-agent", DecisionType.BLOCK))
        self.assertGreaterEqual(rep.score_for("very-bad-agent"), 0.0)


if __name__ == "__main__":
    unittest.main()
