"""External threat-intelligence lookups: sanctions lists, phishing/scam
address databases, honeypot detectors. Ships with an empty in-memory set —
wire up a real feed (OFAC SDN, Chainalysis, TRM, GoPlus, community
scam-address lists) before production use. A hit here is treated as
conclusive, so keep the false-positive rate near zero for whatever source
you plug in.
"""
from __future__ import annotations

from typing import List, Optional

from guardian.core.models import Signal

# Populate from a real sanctions/threat feed. Lower-cased addresses.
SANCTIONED_ADDRESSES: set = set()


class ThreatIntelligence:
    source = "threat_intel"

    def check(self, wallet: str, target: Optional[str] = None) -> List[Signal]:
        signals: List[Signal] = []
        for label, addr in (("wallet", wallet), ("target", target)):
            if addr and addr.lower() in SANCTIONED_ADDRESSES:
                signals.append(Signal(
                    source=self.source, name="sanctioned_address", score=100, weight=10.0,
                    confidence=1.0,
                    reason=f"{label.capitalize()} address matches a sanctions/threat list entry",
                ))
        return signals
