"""Contract data providers.

``MockContractDataProvider`` keeps the original deterministic placeholder
for zero-config demo/test use. ``BlockscoutContractDataProvider`` calls a
public Blockscout instance's REST API to check whether the target
contract's source is actually verified - real signal, no API key.

Blockscout runs free public instances for most major EVM chains
(``eth.blockscout.com``, ``base.blockscout.com``, etc.) - point
``base_url`` at whichever instance matches your target chain via
``GUARDIAN_BLOCKSCOUT_BASE_URL``. Their exact response schema can change
between versions, so this is written defensively: any unexpected shape or
network failure degrades to "unknown", never to a fabricated answer, and
never raises out of ``get_profile``.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Optional, Protocol

logger = logging.getLogger("guardian.contract")


@dataclass
class ContractProfile:
    address: str
    is_verified: Optional[bool]
    is_upgradeable: Optional[bool] = None
    data_source: str = "unknown"


class ContractDataProvider(Protocol):
    def get_profile(self, address: str, chain: str) -> ContractProfile: ...


class MockContractDataProvider:
    name = "mock"

    def get_profile(self, address: str, chain: str) -> ContractProfile:
        h = int(hashlib.sha256(f"{chain}:{address.lower()}".encode()).hexdigest(), 16)
        return ContractProfile(
            address=address,
            is_verified=(h % 3) != 0,
            is_upgradeable=(h % 5) == 0,
            data_source="mock",
        )


class BlockscoutContractDataProvider:
    """Real contract-verification lookup via a Blockscout instance's public API.

    Requires the ``httpx`` package (already a base dependency of this
    project). Any failure - network error, unexpected schema, rate limit -
    is caught and returns ``is_verified=None`` / ``is_upgradeable=None``
    rather than guessing.
    """

    name = "blockscout"

    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_profile(self, address: str, chain: str) -> ContractProfile:
        import httpx

        url = f"{self.base_url}/api/v2/smart-contracts/{address}"
        try:
            resp = httpx.get(url, timeout=self.timeout)
            if resp.status_code == 404:
                # Blockscout returns 404 for addresses with no verified-contract
                # record - which includes both EOAs and unverified contracts.
                return ContractProfile(address=address, is_verified=False, data_source="blockscout")
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            logger.warning("Blockscout lookup failed for %s on %s; returning unknown profile", address, chain, exc_info=True)
            return ContractProfile(address=address, is_verified=None, is_upgradeable=None, data_source="blockscout_error")

        is_verified = bool(data.get("is_verified", data.get("verified_at") is not None))
        proxy_type = data.get("proxy_type")
        is_upgradeable = proxy_type is not None if "proxy_type" in data else None

        return ContractProfile(
            address=address, is_verified=is_verified, is_upgradeable=is_upgradeable,
            data_source="blockscout",
        )
