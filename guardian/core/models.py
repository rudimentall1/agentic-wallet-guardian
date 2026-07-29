"""Core domain models shared across the Guardian decision pipeline.

These are deliberately implemented with the standard library
(dataclasses/enum) rather than pydantic, so the decision core has zero
external dependencies and can be unit-tested, embedded, or ported without
pulling in a web framework. Pydantic is used only at the API boundary
(see api/schemas.py) to validate incoming HTTP requests.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Any, Dict, List


class DecisionType(str, Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    BLOCK = "BLOCK"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Signal:
    """A single piece of evidence produced by an analyzer.

    `score` is the signal's contribution to overall risk on a 0-100 scale
    (0 = no risk, 100 = maximum risk). `weight` controls how much this
    signal contributes to the fused score relative to others. `confidence`
    reflects how much the analyzer trusts its own data (0.0-1.0);
    low-confidence signals are automatically down-weighted by the fusion
    engine instead of treated as equally reliable evidence.
    """

    source: str
    name: str
    score: float
    weight: float = 1.0
    confidence: float = 1.0
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyViolation:
    """A business-rule violation, independent of the statistical risk score.

    severity="BLOCK" always forces a BLOCK decision regardless of the fused
    risk score. severity="WARN" nudges the decision toward WARN and is
    surfaced in the explanation, but does not by itself force BLOCK.
    """

    rule: str
    message: str
    severity: str = "WARN"  # WARN | BLOCK


@dataclass
class Decision:
    decision: DecisionType
    risk_score: float
    risk_level: RiskLevel
    confidence: float
    explanation: List[str]
    signals: List[Signal]
    policy_violations: List[PolicyViolation]
    agent_id: str
    intent_id: str
    created_at: float = field(default_factory=time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "risk_score": round(self.risk_score, 2),
            "risk_level": self.risk_level.value,
            "confidence": round(self.confidence, 2),
            "explanation": self.explanation,
            "signals": [
                {
                    "source": s.source,
                    "name": s.name,
                    "score": round(s.score, 2),
                    "weight": s.weight,
                    "confidence": s.confidence,
                    "reason": s.reason,
                }
                for s in self.signals
            ],
            "policy_violations": [
                {"rule": v.rule, "message": v.message, "severity": v.severity}
                for v in self.policy_violations
            ],
            "agent_id": self.agent_id,
            "intent_id": self.intent_id,
            "created_at": self.created_at,
        }
