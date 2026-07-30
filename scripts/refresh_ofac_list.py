#!/usr/bin/env python3
"""Refresh data/threat_lists/sanctioned_addresses.json from OFAC's public
SDN Advanced list (the machine-readable feed that includes digital-
currency addresses tied to sanctioned entities).

IMPORTANT - read before running:

    This script was written and reviewed for correctness, but has NOT
    been run end-to-end against the live OFAC endpoint from this
    codebase's build environment (no network access to treasury.gov
    there). Before relying on it: run it once yourself, eyeball the
    resulting diff to data/threat_lists/sanctioned_addresses.json, and
    verify the source URL below still matches OFAC's current publishing
    location at https://ofac.treasury.gov/sanctions-list-service - these
    URLs and the XML schema have changed before and can change again.

Usage:

    python scripts/refresh_ofac_list.py
    python scripts/refresh_ofac_list.py --file already-downloaded-sdn.xml
    python scripts/refresh_ofac_list.py --dry-run

Schedule this (cron / systemd timer) rather than running it inline in the
request path - it's a batch refresh of a local file, not a live lookup.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict
from urllib.request import urlopen

DEFAULT_SOURCE_URL = "https://www.treasury.gov/ofac/downloads/sdn_advanced.xml"
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "threat_lists" / "sanctioned_addresses.json"

# OFAC's advanced SDN XML tags digital-currency identifiers with an ID type
# whose text contains "Digital Currency Address" (e.g. "Digital Currency
# Address - XBT", "... - ETH", "... - USDT"). We match on that substring
# rather than an exact enum, since the currency suffix varies per entry and
# OFAC has added new ones over time.
ID_TYPE_MARKER = "Digital Currency Address"
ADDRESS_LIKE = re.compile(r"^[a-zA-Z0-9]{20,64}$")


def fetch_xml(source: str) -> bytes:
    if source.startswith("http://") or source.startswith("https://"):
        with urlopen(source, timeout=30) as resp:  # noqa: S310 - fixed, documented source
            return resp.read()
    return Path(source).read_bytes()


def extract_addresses(xml_bytes: bytes) -> Dict[str, str]:
    """Returns {lowercased_address: label}. Best-effort XML walk that
    tolerates the OFAC advanced-XML namespace without hardcoding it."""
    root = ET.fromstring(xml_bytes)
    found: Dict[str, str] = {}

    for id_elem in root.iter():
        tag = id_elem.tag.rsplit("}", 1)[-1]  # strip XML namespace
        if tag not in ("id", "Id", "ID"):
            continue
        children = {c.tag.rsplit("}", 1)[-1]: (c.text or "").strip() for c in id_elem}
        id_type = children.get("idType", "") or children.get("IDType", "")
        if ID_TYPE_MARKER not in id_type:
            continue
        value = children.get("idNumber", "") or children.get("IDNumber", "")
        if not value or not ADDRESS_LIKE.match(value):
            continue
        found[value.lower()] = f"OFAC SDN - {id_type}"

    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", help="Path to an already-downloaded sdn_advanced.xml, instead of fetching it")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--dry-run", action="store_true", help="Print what would change, write nothing")
    args = parser.parse_args()

    try:
        xml_bytes = fetch_xml(args.file or args.source_url)
    except Exception as exc:
        print(f"Failed to fetch/read source: {exc}", file=sys.stderr)
        return 1

    try:
        new_entries = extract_addresses(xml_bytes)
    except ET.ParseError as exc:
        print(f"Failed to parse XML - has OFAC's schema changed? ({exc})", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    existing: Dict[str, str] = {}
    if output_path.exists():
        existing = json.loads(output_path.read_text())

    merged = {**existing, **new_entries}
    added = set(merged) - set(existing)
    removed = set(existing) - set(new_entries) if new_entries else set()

    print(f"Parsed {len(new_entries)} digital-currency addresses from source.")
    print(f"New entries to add: {len(added)}")
    if removed:
        print(f"Note: {len(removed)} previously-loaded entries are no longer in the source feed "
              f"(kept - delist manually if you've confirmed removal is correct).")

    if args.dry_run:
        print("Dry run - no file written.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dict(sorted(merged.items())), indent=2) + "\n")
    print(f"Wrote {len(merged)} total entries to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
