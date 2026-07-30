# Threat lists

These three files back Guardian's `threat_intel` and `contract` signal
sources. They ship **empty on purpose** - populating them with invented or
unverified addresses would be worse than shipping nothing, since a hit on
these lists is treated as conclusive (`confidence=1.0` for
`sanctioned_addresses.json`, forced weight for `malicious_contracts.json`).

This is also the point of the self-hosted design: these are plain JSON
files on your own disk, not a call to a third-party API. Nothing about
which addresses you're checking ever leaves your infrastructure for this
signal.

## Format

Each file is a flat JSON object: lower-cased address → short label/reason.

```json
{
  "0xabc0000000000000000000000000000000abc0": "OFAC SDN list entry, added 2026-01-15",
  "0xdef0000000000000000000000000000000def0": "Reported rug-pull contract, see incident #142"
}
```

- `sanctioned_addresses.json` - checked against both the initiating wallet
  and the transaction target by `ThreatIntelligence`.
- `malicious_contracts.json` / `verified_contracts.json` - checked against
  the transaction target by `ContractAnalyzer`, before it falls back to
  whichever `ContractDataProvider` you've configured.

## Where to source entries

- **OFAC SDN list** (US sanctions): public, updated regularly. See
  `scripts/refresh_ofac_list.py` for an automated fetch-and-merge script -
  run it yourself and schedule it (cron/systemd timer), since this
  sandbox's network access does not include treasury.gov.
- **Community scam-address databases** (e.g. Chainabuse, CryptoScamDB
  exports, your own incident tracker) - many publish CSV/JSON exports you
  can transform into this schema.
- **Your own findings** - anything your team has directly investigated and
  confirmed.

## Reloading

`AddressList` loads the file once at process start. Call `.reload()` on
the instance (or restart the process) after editing a file to pick up
changes without a code change - e.g. from a scheduled refresh job.
