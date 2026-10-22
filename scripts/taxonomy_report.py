"""Print taxonomy migration coverage for the current watchlist."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import WATCHLIST  # noqa: E402


def main() -> int:
    total = len(WATCHLIST)
    normalized_sector = sum(bool(item.get("sector_id")) for item in WATCHLIST)
    normalized_industry = sum(bool(item.get("industry_id")) for item in WATCHLIST)
    normalized_theme = sum(bool(item.get("theme_ids")) for item in WATCHLIST)
    normalized_tags = sum(bool(item.get("tag_ids")) for item in WATCHLIST)
    legacy_tags = sum(bool(item.get("tags")) for item in WATCHLIST)

    print(f"watchlist entries: {total}")
    print(f"sector_id coverage: {normalized_sector}/{total}")
    print(f"industry_id coverage: {normalized_industry}/{total}")
    print(f"theme_ids coverage: {normalized_theme}/{total}")
    print(f"tag_ids coverage: {normalized_tags}/{total}")
    print(f"legacy tags coverage: {legacy_tags}/{total}")
    print("migration status: dual-write; legacy fields remain supported")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
