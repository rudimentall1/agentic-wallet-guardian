"""Wallet intelligence analyzer.

Delegates data collection to a ``WalletDataProvider`` (see
``guardian/intelligence/wallet/providers.py``) so the risk logic here is
identical whether the profile came from the mock generator or a real
on-chain RPC lookup. Select the provider via ``GUARDIAN_WALLET_PROVIDER``
- see ``guardian/config.py`` - or pass one in directly for testing.
"""
from __future__ import annotations

from typing import List, Optional

from guardian.core.models import Signal
from guardian.intelligence.wallet.providers import (
    MockWalletDataProvider,
    RpcWalletDataProvider,
    WalletDataProvider,
)


def build_wallet_provider(config) -> WalletDataProvider:
    if config.wallet_provider == "rpc":
        return RpcWalletDataProvider(
            rpc_urls=config.rpc_urls,
            estimate_age=config.estimate_wallet_age,
            timeout=config.provider_timeout_seconds,
        )
    return MockWalletDataProvider()


class WalletAnalyzer:
    """Produces risk signals about the wallet initiating the action."""

    source = "wallet"

    def __init__(self, provider: Optional[WalletDataProvider] = None):
        self.provider = provider or MockWalletDataProvider()

    def analyze(self, address: str, chain: str) -> List[Signal]:
        profile = self.provider.get_profile(address, chain)
        signals: List[Signal] = []
        mock_note = " (mock data source)" if profile.data_source == "mock" else ""

        if profile.is_flagged:
            signals.append(Signal(
                source=self.source, name="flagged_wallet", score=95, weight=3.0,
                confidence=0.6, reason=f"Wallet matches a known risk indicator{mock_note}",
            ))

        if profile.age_days is None:
            # Genuinely unknown is itself informative for a security decision:
            # it should nudge caution, not be silently skipped.
            signals.append(Signal(
                source=self.source, name="wallet_age_unknown", score=25, weight=0.6,
                confidence=0.4,
                reason="Wallet age could not be determined from the configured data source",
            ))
        elif profile.age_days < 3:
            signals.append(Signal(
                source=self.source, name="new_wallet", score=70, weight=1.5,
                confidence=0.8, reason=f"Wallet is very new ({profile.age_days} days old){mock_note}",
            ))
        elif profile.age_days < 30:
            signals.append(Signal(
                source=self.source, name="young_wallet", score=35, weight=1.0,
                confidence=0.8, reason=f"Wallet is young ({profile.age_days} days old){mock_note}",
            ))
        else:
            signals.append(Signal(
                source=self.source, name="established_wallet", score=5, weight=1.0,
                confidence=0.8,
                reason=f"Wallet has an established history ({profile.age_days} days old){mock_note}",
            ))

        if profile.tx_count is None:
            signals.append(Signal(
                source=self.source, name="tx_count_unknown", score=20, weight=0.5,
                confidence=0.4,
                reason="Wallet transaction count could not be determined from the configured data source",
            ))
        elif profile.tx_count < 3:
            signals.append(Signal(
                source=self.source, name="low_activity", score=40, weight=0.8,
                confidence=0.7, reason=f"Wallet has very little on-chain activity{mock_note}",
            ))

        if profile.is_contract:
            signals.append(Signal(
                source=self.source, name="wallet_is_contract", score=30, weight=0.7,
                confidence=0.85,
                reason="The initiating address is a contract, not an externally-owned account",
            ))

        return signals
