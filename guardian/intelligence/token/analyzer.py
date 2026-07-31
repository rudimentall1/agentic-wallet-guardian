"""Token intelligence analyzer.

Delegates liquidity data to a ``TokenDataProvider`` - the mock generator
by default, or ``DexScreenerTokenDataProvider`` for real liquidity data.
Select via ``GUARDIAN_TOKEN_PROVIDER`` (``mock`` | ``dexscreener``).
"""
from __future__ import annotations

from typing import List, Optional

from guardian.core.models import Signal
from guardian.intelligence.token.providers import (
    DexScreenerTokenDataProvider,
    MockTokenDataProvider,
    TokenDataProvider,
)

# Real, not mock: widely-held major assets don't need a liquidity lookup at
# all - skipping the provider call here also means one fewer external
# request on the most common path (agents swapping into/out of stables).
MAJOR_TOKENS = {"ETH", "WETH", "USDC", "USDT", "DAI", "WBTC", "SOL", "USDS"}


def build_token_provider(config) -> TokenDataProvider:
    if config.token_provider == "dexscreener":
        return DexScreenerTokenDataProvider(
            base_url=config.dexscreener_base_url, timeout=config.provider_timeout_seconds,
        )
    return MockTokenDataProvider()


class TokenAnalyzer:
    source = "token"

    def __init__(self, provider: Optional[TokenDataProvider] = None):
        self.provider = provider or MockTokenDataProvider()

    def analyze(self, symbol: Optional[str], chain: str) -> List[Signal]:
        if not symbol:
            return []

        if symbol.upper() in MAJOR_TOKENS:
            return [Signal(
                source=self.source, name="major_token", score=2, weight=1.0,
                confidence=0.95, reason=f"{symbol.upper()} is a widely-held, liquid asset",
            )]

        profile = self.provider.get_liquidity_profile(symbol, chain)
        signals: List[Signal] = []
        mock_note = " (mock data source)" if profile.data_source == "mock" else ""

        if profile.match_confidence < 0.5:
            signals.append(Signal(
                source=self.source, name="token_match_uncertain", score=20, weight=0.4,
                confidence=0.3,
                reason=f"Could not confidently match ticker '{symbol}' to a specific on-chain pair "
                       f"- ticker symbols are not unique and are often impersonated",
            ))
            return signals

        if profile.liquidity_usd is None:
            signals.append(Signal(
                source=self.source, name="liquidity_unknown", score=15, weight=0.4,
                confidence=0.4,
                reason="Token liquidity could not be determined from the configured data source",
            ))
        elif profile.is_concentrated:
            signals.append(Signal(
                source=self.source, name="thin_liquidity", score=60, weight=1.3,
                confidence=0.7,
                reason=f"Token liquidity is thin (${profile.liquidity_usd:,.0f}){mock_note} "
                       f"- price impact and rug risk are both higher",
            ))
        else:
            signals.append(Signal(
                source=self.source, name="adequate_liquidity", score=5, weight=0.6,
                confidence=0.7, reason=f"Token liquidity looks adequate (${profile.liquidity_usd:,.0f}){mock_note}",
            ))

        return signals
