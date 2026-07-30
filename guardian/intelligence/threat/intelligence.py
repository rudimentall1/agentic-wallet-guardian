"""External threat-intelligence lookups: sanctions lists, phishing/scam
address databases, honeypot detectors.

Backed by a local, operator-maintained JSON file (see
``guardian/intelligence/threat/blocklist.py``) rather than an empty
in-memory set. A hit here is treated as conclusive, so keep the
false-positive rate near zero for whatever you load into that file.
"""
from __future__ import annotations

from typing import List, Optional

from guardian.core.models import Signal
from guardian.intelligence.threat.blocklist import AddressList


class ThreatIntelligence:
    source = "threat_intel"

    def __init__(self, sanctioned: Optional[AddressList] = None):
        self.sanctioned = sanctioned or AddressList("data/threat_lists/sanctioned_addresses.json")

    def check(self, wallet: str, target: Optional[str] = None) -> List[Signal]:
        signals: List[Signal] = []
        for label, addr in (("wallet", wallet), ("target", target)):
            if addr and addr in self.sanctioned:
                reason = self.sanctioned.label_for(addr)
                signals.append(Signal(
                    source=self.source, name="sanctioned_address", score=100, weight=10.0,
                    confidence=1.0,
                    reason=f"{label.capitalize()} address matches a threat list entry ({reason})",
                ))
        return signals
