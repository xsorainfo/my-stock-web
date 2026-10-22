"""Report taxonomy migration coverage for config and generated data."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import WATCHLIST  # noqa: E402


def _coverage(items: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "sector_id": sum(bool(item.get("sector_id")) for item in items),
        "industry_id": sum(bool(item.get("industry_id")) for item in items),
        "theme_ids": sum(bool(item.get("theme_ids")) for item in items),
        "tag_ids": sum(bool(item.get("tag_ids")) for item in items),
        "legacy_tags": sum(bool(item.get("tags")) for item in items),
    }


def _print_report(label: str, items: list[dict[str, Any]]) -> None:
    coverage = _coverage(items)
    total = len(items)
    print(f"[{label}] watchlist entries: {total}")
    for key in ("sector_id", "industry_id", "theme_ids", "tag_ids", "legacy_tags"):
        print(f"[{label}] {key} coverage: {coverage[key]}/{total}")
    print(f"[{label}] normalized entries: {sum(bool(item.get('taxonomy')) for item in items)}/{total}")


def main() -> int:
    _print_report("config.WATCHLIST", list(WATCHLIST))

    data_path = ROOT / "data" / "data.json"
    if data_path.exists():
        try:
            payload = json.loads(data_path.read_text(encoding="utf-8"))
            generated = payload.get("stocks") or payload.get("watchlist") or []
            if isinstance(generated, list):
                _print_report("data/data.json", generated)
            else:
                print("[data/data.json] watchlist payload is not a list")
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[data/data.json] unavailable: {exc}")
    else:
        print("[data/data.json] not found")

    print("migration status: dual-write; legacy fields remain supported")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
