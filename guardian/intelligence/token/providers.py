"""Token data providers.

``MockTokenDataProvider`` keeps the original deterministic placeholder.
``DexScreenerTokenDataProvider`` calls DexScreener's free, no-API-key
public search endpoint to get real liquidity data for a token symbol.

Matching a bare ticker symbol to the right on-chain pair is inherently
fuzzy (many unrelated tokens share a symbol like "PEPE" across chains and
scammers deliberately mint look-alike tickers) - this provider picks the
pair with the highest liquidity on the requested chain as its best guess
and says so in the profile, rather than silently pretending the match is
certain. For anything where that ambiguity matters, match by contract
address instead of symbol.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Optional, Protocol

logger = logging.getLogger("guardian.token")


@dataclass
class TokenLiquidityProfile:
    symbol: str
    liquidity_usd: Optional[float]
    is_concentrated: Optional[bool]
    data_source: str = "unknown"
    match_confidence: float = 1.0


class TokenDataProvider(Protocol):
    def get_liquidity_profile(self, symbol: str, chain: str) -> TokenLiquidityProfile: ...


class MockTokenDataProvider:
    name = "mock"

    def get_liquidity_profile(self, symbol: str, chain: str) -> TokenLiquidityProfile:
        h = int(hashlib.sha256(f"{chain}:{symbol.lower()}".encode()).hexdigest(), 16)
        return TokenLiquidityProfile(
            symbol=symbol, liquidity_usd=None, is_concentrated=(h % 4) == 0, data_source="mock",
        )


# Below this, treat liquidity as "concentrated / thin" - crossing a
# scammer's usual bar of a few hundred to a few thousand dollars of fake
# liquidity to make a token look tradeable.
THIN_LIQUIDITY_USD_THRESHOLD = 20_000.0


class DexScreenerTokenDataProvider:
    """Real liquidity data via DexScreener's public search API.

    Requires ``httpx`` (already a base dependency). DexScreener's API is
    free and keyless, but - like any third-party API - its exact response
    schema and rate limits can change; verify against
    https://docs.dexscreener.com before depending on this in production.
    Any failure degrades to ``liquidity_usd=None`` / unknown, never a
    fabricated number.
    """

    name = "dexscreener"

    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_liquidity_profile(self, symbol: str, chain: str) -> TokenLiquidityProfile:
        import httpx

        url = f"{self.base_url}/latest/dex/search"
        try:
            resp = httpx.get(url, params={"q": symbol}, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            pairs = data.get("pairs") or []
        except Exception:
            logger.warning("DexScreener lookup failed for %s on %s; returning unknown profile", symbol, chain, exc_info=True)
            return TokenLiquidityProfile(symbol=symbol, liquidity_usd=None, is_concentrated=None, data_source="dexscreener_error")

        chain_pairs = [p for p in pairs if str(p.get("chainId", "")).lower() == chain.lower()]
        candidates = chain_pairs or pairs
        if not candidates:
            return TokenLiquidityProfile(
                symbol=symbol, liquidity_usd=None, is_concentrated=None,
                data_source="dexscreener", match_confidence=0.0,
            )

        best = max(candidates, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0.0)
        liquidity_usd = (best.get("liquidity") or {}).get("usd")
        match_confidence = 0.8 if chain_pairs else 0.4  # lower confidence if we had to guess across chains

        return TokenLiquidityProfile(
            symbol=symbol,
            liquidity_usd=liquidity_usd,
            is_concentrated=(liquidity_usd is not None and liquidity_usd < THIN_LIQUIDITY_USD_THRESHOLD),
            data_source="dexscreener",
            match_confidence=match_confidence,
        )
