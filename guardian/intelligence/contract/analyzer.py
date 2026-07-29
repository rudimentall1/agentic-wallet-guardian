"""Contract intelligence analyzer.

Ships with a small in-memory allow/deny list as a real (if minimal)
starting point, plus a deterministic mock fallback for anything unlisted.
Replace the fallback with a real registry (verified-contract database,
bytecode/upgrade-pattern analysis, GoPlus/Chainalysis contract-security
API, or your own audit database) before production use.
"""
from __future__ import annotations

import hashlib
from typing import List, Optional

from guardian.core.models import Signal

# Populate these from a real registry / your own audit findings.
KNOWN_SAFE_CONTRACTS: dict = {}
KNOWN_MALICIOUS_CONTRACTS: dict = {}


class ContractAnalyzer:
    source = "contract"

    def analyze(self, contract_address: Optional[str], chain: str) -> List[Signal]:
        if not contract_address:
            return []

        addr = contract_address.lower()

        if addr in KNOWN_MALICIOUS_CONTRACTS:
            return [Signal(
                source=self.source, name="known_malicious_contract", score=100, weight=5.0,
                confidence=0.95,
                reason=f"Target contract is on the deny-list ({KNOWN_MALICIOUS_CONTRACTS[addr]})",
            )]

        if addr in KNOWN_SAFE_CONTRACTS:
            return [Signal(
                source=self.source, name="known_safe_contract", score=2, weight=1.0,
                confidence=0.9,
                reason=f"Target contract is a known verified contract ({KNOWN_SAFE_CONTRACTS[addr]})",
            )]

        # Unknown contract: deterministic mock heuristics stand in for real
        # bytecode / verification / upgrade-pattern analysis.
        # TODO(production): replace with a real contract-security lookup.
        h = int(hashlib.sha256(f"{chain}:{addr}".encode()).hexdigest(), 16)
        is_verified = (h % 3) != 0  # ~66% "verified" in mock data
        is_upgradeable = (h % 5) == 0  # ~20% "upgradeable" in mock data

        signals: List[Signal] = []
        if is_verified:
            signals.append(Signal(
                source=self.source, name="verified_contract", score=10, weight=0.8,
                confidence=0.6, reason="Target contract source is verified (mock data source)",
            ))
        else:
            signals.append(Signal(
                source=self.source, name="unverified_contract", score=55, weight=1.5,
                confidence=0.6, reason="Target contract source is not verified (mock data source)",
            ))

        if is_upgradeable:
            signals.append(Signal(
                source=self.source, name="upgradeable_contract", score=40, weight=1.2,
                confidence=0.5,
                reason="Contract uses an upgradeable proxy pattern — logic can change after approval",
            ))

        return signals
