"""Dry-run smoke test: verify installer files pin the expected uv version and checksums match.

No installation is performed. This test reads local files only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"
INSTALL_PS1 = REPO_ROOT / "install.ps1"
CHECKSUMS_TXT = REPO_ROOT / "install" / "checksums.txt"
CHECKSUMS_JSON = REPO_ROOT / "install" / "checksums.json"

EXPECTED_UV_VERSION = "0.11.16"
STALE_UV_DEFAULT = ":-0.11.7}"  # the old pinned default pattern


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _parse_checksums_txt() -> dict[str, str]:
    result = {}
    for line in CHECKSUMS_TXT.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 2:
            digest, name = parts
            result[name.lstrip("*")] = digest
    return result


def test_install_sh_pins_expected_uv_version():
    """install.sh must pin uv 0.11.16, not the stale 0.11.7 default."""
    src = INSTALL_SH.read_text(encoding="utf-8")
    assert f":-{EXPECTED_UV_VERSION}" + "}" in src, (
        f"install.sh must contain SPARK_UV_VERSION default of {EXPECTED_UV_VERSION}"
    )


def test_install_ps1_pins_expected_uv_version():
    """install.ps1 must pin the same uv version."""
    src = INSTALL_PS1.read_text(encoding="utf-8")
    assert EXPECTED_UV_VERSION in src, (
        f"install.ps1 must reference uv {EXPECTED_UV_VERSION}"
    )


def test_no_stale_uv_default_in_install_sh():
    """The stale 0.11.7 default pattern must not appear in install.sh."""
    src = INSTALL_SH.read_text(encoding="utf-8")
    assert STALE_UV_DEFAULT not in src, (
        "stale uv 0.11.7 default must be absent from install.sh"
    )


def test_install_sh_checksum_matches_checksums_txt():
    """SHA256 of install.sh must match the value recorded in checksums.txt."""
    expected = _parse_checksums_txt().get("install.sh")
    assert expected is not None, "checksums.txt must contain install.sh entry"
    actual = _sha256(INSTALL_SH)
    assert actual == expected, f"install.sh checksum mismatch: {actual} != {expected}"


def test_install_ps1_checksum_matches_checksums_txt():
    """SHA256 of install.ps1 must match the value recorded in checksums.txt."""
    expected = _parse_checksums_txt().get("install.ps1")
    assert expected is not None, "checksums.txt must contain install.ps1 entry"
    actual = _sha256(INSTALL_PS1)
    assert actual == expected, f"install.ps1 checksum mismatch: {actual} != {expected}"


def test_checksums_json_consistent_with_checksums_txt():
    """checksums.json must agree with checksums.txt on both file hashes."""
    txt = _parse_checksums_txt()
    data = json.loads(CHECKSUMS_JSON.read_text(encoding="utf-8"))
    for entry in data.get("files", []):
        name = entry["path"].split("/")[-1]
        if name in txt:
            assert entry["sha256"] == txt[name], (
                f"checksums.json and checksums.txt disagree on {name}: "
                f"{entry['sha256']} vs {txt[name]}"
            )
