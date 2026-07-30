"""Wallet data providers.

``WalletDataProvider`` is the interface ``WalletAnalyzer`` depends on. Two
implementations ship here:

- ``MockWalletDataProvider``: the original deterministic hash-based
  placeholder. Zero dependencies, zero network calls, fully offline -
  good for tests, demos, and CI. **Not a real risk signal.**
- ``RpcWalletDataProvider``: talks to a real JSON-RPC node (your own, or
  a provider you trust) via ``web3.py``. No API key required beyond the
  RPC endpoint itself.

Select which one ``DecisionEngine`` uses via ``GUARDIAN_WALLET_PROVIDER``
(``mock`` | ``rpc``) - see ``guardian/config.py``. Nothing outside this
file needs to know which one is active; both return the same
``WalletProfile`` shape, with ``None`` for any field a provider genuinely
cannot determine (never a guessed value standing in for missing data).
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Dict, Optional, Protocol

logger = logging.getLogger("guardian.wallet")


@dataclass
class WalletProfile:
    address: str
    age_days: Optional[int]
    tx_count: Optional[int]
    is_contract: Optional[bool] = None
    is_flagged: bool = False
    data_source: str = "unknown"


class WalletDataProvider(Protocol):
    def get_profile(self, address: str, chain: str) -> WalletProfile: ...


class MockWalletDataProvider:
    """Deterministic placeholder, derived from a hash of the address.

    Ships as the default so Guardian is runnable end-to-end with zero
    setup. This is an honest stand-in, not a real risk signal - switch to
    ``RpcWalletDataProvider`` (or write your own provider against a paid
    intelligence API) before using decisions in production.
    """

    name = "mock"

    def get_profile(self, address: str, chain: str) -> WalletProfile:
        h = int(hashlib.sha256(f"{chain}:{address}".encode()).hexdigest(), 16)
        age_days = h % 900
        tx_count = (h // 900) % 5000
        is_flagged = (h % 97) == 0
        return WalletProfile(
            address=address, age_days=age_days, tx_count=tx_count,
            is_flagged=is_flagged, data_source="mock",
        )


class RpcWalletDataProvider:
    """Real on-chain data via direct JSON-RPC (``web3.py``).

    What this genuinely gives you, with no API key and no third-party
    intelligence vendor:

    - ``is_contract``: reliable - one ``eth_getCode`` call.
    - ``tx_count``: the account's current *nonce*
      (``eth_getTransactionCount``). This is a real number, but it only
      counts outgoing transactions - a wallet that only ever *received*
      funds will show 0 here even if it holds a large balance. Treat it
      as "outgoing activity count", not "total activity".
    - ``age_days``: **not available** from a plain, non-archive RPC
      endpoint, so this is ``None`` unless you explicitly enable
      ``GUARDIAN_RPC_ESTIMATE_AGE=true`` *and* point ``rpc_url`` at an
      archive node. When enabled, it binary-searches historical blocks
      for the first one where the account has a non-zero nonce or
      balance. Most free public RPC endpoints are not archive nodes and
      will error on old historical queries - that failure is caught and
      surfaces as "age unknown", never as a fabricated number.

    Requires the ``web3`` package (see ``requirements-chain.txt``); the
    import is deferred so installing it is only necessary if you actually
    select this provider.
    """

    name = "rpc"

    def __init__(self, rpc_urls: Dict[str, str], estimate_age: bool = False, timeout: float = 5.0):
        self.rpc_urls = rpc_urls
        self.estimate_age = estimate_age
        self.timeout = timeout
        self._clients: Dict[str, object] = {}

    def _client(self, chain: str):
        if chain in self._clients:
            return self._clients[chain]
        url = self.rpc_urls.get(chain)
        if not url:
            raise ValueError(
                f"No RPC URL configured for chain '{chain}'. Set GUARDIAN_RPC_{chain.upper()}."
            )
        try:
            from web3 import Web3
        except ImportError as exc:  # pragma: no cover - exercised via requirements-chain
            raise ImportError(
                "RpcWalletDataProvider requires the 'web3' package. "
                "Install it with: pip install -r requirements-chain.txt"
            ) from exc

        w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": self.timeout}))
        self._clients[chain] = w3
        return w3

    def get_profile(self, address: str, chain: str) -> WalletProfile:
        try:
            w3 = self._client(chain)
            checksum = w3.to_checksum_address(address)
            tx_count = w3.eth.get_transaction_count(checksum)
            code = w3.eth.get_code(checksum)
            is_contract = len(code) > 0
        except Exception:
            logger.warning("RPC lookup failed for %s on %s; returning unknown profile", address, chain, exc_info=True)
            return WalletProfile(address=address, age_days=None, tx_count=None, data_source="rpc_error")

        age_days = self._estimate_age_days(w3, checksum) if self.estimate_age else None

        return WalletProfile(
            address=address,
            age_days=age_days,
            tx_count=tx_count,
            is_contract=is_contract,
            data_source="rpc",
        )

    def _estimate_age_days(self, w3, checksum_address: str) -> Optional[int]:
        """Best-effort first-activity block via binary search.

        Requires archive access to historical state. Any failure (common
        on non-archive public endpoints) is swallowed and returns None -
        callers must treat that as "unknown", not "brand new".
        """
        try:
            import time as _time

            def active_at(block_number: int) -> bool:
                nonce = w3.eth.get_transaction_count(checksum_address, block_identifier=block_number)
                if nonce > 0:
                    return True
                balance = w3.eth.get_balance(checksum_address, block_identifier=block_number)
                return balance > 0

            latest_block = w3.eth.block_number
            if not active_at(latest_block):
                return None  # wallet has never transacted / holds nothing

            lo, hi = 0, latest_block
            # Binary search for the earliest block where the account is active.
            for _ in range(32):  # hard cap: log2(latest_block) is ~25 even for L1 mainnet
                if lo >= hi:
                    break
                mid = (lo + hi) // 2
                if active_at(mid):
                    hi = mid
                else:
                    lo = mid + 1

            first_block = w3.eth.get_block(hi)
            latest = w3.eth.get_block(latest_block)
            seconds = latest["timestamp"] - first_block["timestamp"]
            return max(0, int(seconds // 86400))
        except Exception:
            logger.info("Archive-based age estimation unavailable for this RPC endpoint", exc_info=True)
            return None
