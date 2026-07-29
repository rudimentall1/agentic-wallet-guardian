"""Risk Fusion Engine: combines heterogeneous Signals into a single risk
score on a 0-100 scale.

Fusion approach: confidence-weighted average of every signal, with the
*maximum* qualifying individual signal acting as a floor — so one very
strong, high-confidence red flag can't be diluted away by a pile of
low-risk signals from unrelated analyzers.
"""
from __future__ import annotations

from typing import List

from guardian.core.models import RiskLevel, Signal


class RiskFusionEngine:
    # A single signal at/above this score, with confidence at/above the
    # confidence floor, sets a hard minimum on the final fused score
    # regardless of what every other signal says.
    DOMINANT_SIGNAL_THRESHOLD = 90
    DOMINANT_SIGNAL_CONFIDENCE_FLOOR = 0.8

    def fuse(self, signals: List[Signal]) -> float:
        if not signals:
            return 20.0  # no data at all is itself a mild risk factor

        weighted_sum = 0.0
        weight_total = 0.0
        dominant_floor = 0.0

        for s in signals:
            effective_weight = max(s.weight, 0.0) * max(min(s.confidence, 1.0), 0.0)
            weighted_sum += s.score * effective_weight
            weight_total += effective_weight

            if s.score >= self.DOMINANT_SIGNAL_THRESHOLD and s.confidence >= self.DOMINANT_SIGNAL_CONFIDENCE_FLOOR:
                dominant_floor = max(dominant_floor, s.score * 0.9)

        fused = (weighted_sum / weight_total) if weight_total > 0 else 20.0
        fused = max(fused, dominant_floor)
        return max(0.0, min(100.0, fused))

    @staticmethod
    def to_risk_level(score: float) -> RiskLevel:
        if score < 25:
            return RiskLevel.LOW
        if score < 55:
            return RiskLevel.MEDIUM
        if score < 80:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL
