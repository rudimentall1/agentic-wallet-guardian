"""Token intelligence analyzer.

NOTE ON DATA SOURCES: major assets are hard-coded (this part is real and
safe to ship as-is). Everything else falls back to a deterministic mock
heuristic for liquidity concentration — replace ``_liquidity_profile`` with
a real DEX-liquidity / holder-distribution source (DEX Screener, GoPlus
token security API, direct on-chain LP queries) before production use.
"""
from __future__ import annotations

import hashlib
from typing import List, Optional

from guardian.core.models import Signal

MAJOR_TOKENS = {"ETH", "WETH", "USDC", "USDT", "DAI", "WBTC", "SOL", "USDS"}


def _liquidity_profile(token_symbol: str, chain: str) -> bool:
    """Returns True if (mock) liquidity looks concentrated. TODO(production): replace."""
    h = int(hashlib.sha256(f"{chain}:{token_symbol.lower()}".encode()).hexdigest(), 16)
    return (h % 4) == 0  # ~25% mock rate


class TokenAnalyzer:
    source = "token"

    def analyze(self, token_symbol: Optional[str], chain: str) -> List[Signal]:
        if not token_symbol:
            return []

        if token_symbol.upper() in MAJOR_TOKENS:
            return [Signal(
                source=self.source, name="major_token", score=2, weight=1.0,
                confidence=0.95, reason=f"{token_symbol.upper()} is a widely-held, liquid asset",
            )]

        signals = [Signal(
            source=self.source, name="unrecognized_token", score=30, weight=1.0,
            confidence=0.5, reason=f"{token_symbol} is not in the major-asset list (mock data source)",
        )]

        if _liquidity_profile(token_symbol, chain):
            signals.append(Signal(
                source=self.source, name="liquidity_concentration", score=50, weight=1.3,
                confidence=0.5,
                reason="Liquidity for this token appears concentrated in a small number of holders",
            ))

        return signals
