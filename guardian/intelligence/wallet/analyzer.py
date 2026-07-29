"""Wallet intelligence analyzer.

NOTE ON DATA SOURCES: this module ships with a deterministic *mock* profile
generator (``_fetch_wallet_profile``) so the engine is fully runnable and
testable offline, with zero API keys. This is an honest placeholder, not a
real risk signal — replace it with a genuine chain-data integration
(Etherscan/Blockscout API, direct RPC via web3.py, or a paid intelligence
provider such as GoPlus / Chainalysis / TRM) before using this in
production. Nothing else in the pipeline needs to change when you do that
swap: scoring, policy and reasoning only depend on the ``Signal`` objects
returned here, never on how they were produced.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List

from guardian.core.models import Signal


@dataclass
class WalletProfile:
    address: str
    age_days: int
    tx_count: int
    is_flagged: bool


def _fetch_wallet_profile(address: str, chain: str) -> WalletProfile:
    """Deterministic placeholder profile derived from a hash of the address.

    TODO(production): replace with a real chain-data lookup.
    """
    h = int(hashlib.sha256(f"{chain}:{address}".encode()).hexdigest(), 16)
    age_days = h % 900  # 0-900 days
    tx_count = (h // 900) % 5000  # 0-5000 txs
    is_flagged = (h % 97) == 0  # ~1% deterministic "flagged" rate in mock data
    return WalletProfile(address=address, age_days=age_days, tx_count=tx_count, is_flagged=is_flagged)


class WalletAnalyzer:
    """Produces risk signals about the wallet initiating the action."""

    source = "wallet"

    def analyze(self, address: str, chain: str) -> List[Signal]:
        profile = _fetch_wallet_profile(address, chain)
        signals: List[Signal] = []

        if profile.is_flagged:
            signals.append(Signal(
                source=self.source, name="flagged_wallet", score=95, weight=3.0,
                confidence=0.6, reason="Wallet matches a known risk indicator (mock data source)",
            ))

        if profile.age_days < 3:
            signals.append(Signal(
                source=self.source, name="new_wallet", score=70, weight=1.5,
                confidence=0.8, reason=f"Wallet is very new ({profile.age_days} days old)",
            ))
        elif profile.age_days < 30:
            signals.append(Signal(
                source=self.source, name="young_wallet", score=35, weight=1.0,
                confidence=0.8, reason=f"Wallet is young ({profile.age_days} days old)",
            ))
        else:
            signals.append(Signal(
                source=self.source, name="established_wallet", score=5, weight=1.0,
                confidence=0.8,
                reason=f"Wallet has an established history ({profile.age_days} days, {profile.tx_count} txs)",
            ))

        if profile.tx_count < 3:
            signals.append(Signal(
                source=self.source, name="low_activity", score=40, weight=0.8,
                confidence=0.7, reason="Wallet has very little on-chain activity",
            ))

        return signals
