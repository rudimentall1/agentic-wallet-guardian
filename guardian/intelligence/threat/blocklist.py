"""Local, file-based address lists.

This is the self-hosted answer to "sanctions list" / "known malicious
contract registry" / "verified contract registry": a plain JSON file that
lives in *your* deployment, that *you* maintain, and that never requires
sending a wallet address to a third-party API just to check it against a
list. No data about who is being checked ever leaves your infrastructure
for this signal.

Format (one file per list): a flat JSON object mapping a lower-cased
address to a short human-readable label/reason::

    {
        "0xabc123...": "OFAC SDN list entry, added 2026-01-15"
    }

Populate these yourself from whatever sources you trust - OFAC's public
SDN list, Chainalysis/TRM if you have a subscription, community
scam-address databases, or your own incident findings. See
``scripts/refresh_ofac_list.py`` for one example of an automated refresh
script you can run on a schedule (it needs network access to
treasury.gov, which this repo does not assume you have at build time).
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger("guardian.threat")


class AddressList:
    def __init__(self, path: str):
        self.path = Path(path)
        self._entries: Dict[str, str] = {}
        self.reload()

    def reload(self) -> None:
        if not self.path.exists():
            logger.info("Address list %s does not exist yet - treating as empty. "
                        "Create it (see guardian/intelligence/threat/blocklist.py docstring "
                        "for the format) to start using this list.", self.path)
            self._entries = {}
            return
        try:
            raw = json.loads(self.path.read_text())
            if not isinstance(raw, dict):
                raise ValueError("expected a JSON object mapping address -> label")
            self._entries = {str(k).lower(): str(v) for k, v in raw.items()}
        except Exception:
            logger.error("Failed to parse address list %s - treating as empty this run", self.path, exc_info=True)
            self._entries = {}

    def __contains__(self, address: str) -> bool:
        return bool(address) and address.lower() in self._entries

    def label_for(self, address: str) -> Optional[str]:
        return self._entries.get((address or "").lower())

    def __len__(self) -> int:
        return len(self._entries)
