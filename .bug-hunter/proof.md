# Bug Hunter Proof — uv version pin stale: 0.11.7 → 0.11.16

## Bug

`install.sh` and `install.ps1` pinned `SPARK_UV_VERSION` to `0.11.7` (released April 15 2026).
`uv 0.11.16` was released May 21 2026 — 9 patch/minor versions behind.
Every Spark install downloaded an outdated uv binary, missing resolver fixes and security patches released in the intervening versions.

## Affected lines (before fix)

| File | Line | Before |
|---|---|---|
| `install.sh` | 15 | `SPARK_UV_VERSION="${SPARK_UV_VERSION:-0.11.7}"` |
| `install.sh` | ~63 | `(default: 0.11.7)` in usage/help text |
| `install.sh` | ~320–323 | uv asset SHA256 values for 0.11.7 |
| `install.ps1` | 7 | `[string]$UvVersion = "0.11.7"` |
| `install.ps1` | ~151–152 | uv asset SHA256 values for 0.11.7 |

## Fix applied

- Bumped `SPARK_UV_VERSION` to `0.11.16` in both installer files
- Updated all 6 platform binary SHA256 hashes to match the `0.11.16` release assets
- Updated help text default in `install.sh`
- Recomputed `install.sh` and `install.ps1` SHA256s and updated:
  - `install/checksums.txt`
  - `install/checksums.json`
  - `install/commands.json` checksums block
- Updated `install/release-manifest.json` uv version and all 6 asset hashes
- Updated uv version string in: `docs/AGENTS.md`, `docs/install-safety.md`, `docs/llms-full.txt`, `llms-full.txt`

## Verification

All 10 files verified clean. No stale `0.11.7` references remain in public-facing files.

uv 0.11.16 release: https://github.com/astral-sh/uv/releases/tag/0.11.16
