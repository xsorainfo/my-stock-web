"""Validate the normalized taxonomy without changing runtime data."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import WATCHLIST  # noqa: E402


def load_json(path: str):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    sector_catalog = load_json("data/sector_catalog.json")
    theme_catalog = load_json("data/theme_catalog.json")
    tag_catalog = load_json("data/tag_catalog.json")
    sector_ids = {item["id"] for item in sector_catalog.get("sectors", [])}
    industry_ids = {
        industry["id"]
        for sector in sector_catalog.get("sectors", [])
        for industry in sector.get("industries", [])
    }
    theme_ids = {item["id"] for item in theme_catalog.get("themes", [])}
    tag_ids = {item["id"] for item in tag_catalog.get("tags", [])}

    errors = []
    seen = set()
    for item in WATCHLIST:
        symbol = item.get("symbol", "")
        if symbol in seen:
            errors.append(f"duplicate symbol: {symbol}")
        seen.add(symbol)

        sector_id = str(item.get("sector_id") or item.get("sector") or "")
        industry_id = str(item.get("industry_id") or item.get("industry") or "")
        if sector_id and sector_id not in sector_ids:
            errors.append(f"{symbol}: unknown sector_id {sector_id}")
        if industry_id and industry_id not in industry_ids:
            errors.append(f"{symbol}: unknown industry_id {industry_id}")
        tags = item.get("tags") or []
        if not isinstance(tags, list):
            errors.append(f"{symbol}: tags must be a list")
        for tag_id in item.get("tag_ids") or []:
            if tag_id not in tag_ids:
                errors.append(f"{symbol}: unknown tag_id {tag_id}")

        for theme_id in item.get("theme_ids") or []:
            if theme_id not in theme_ids:
                errors.append(f"{symbol}: unknown theme_id {theme_id}")

    print(f"checked {len(WATCHLIST)} watchlist entries")
    if errors:
        print(f"found {len(errors)} taxonomy issues")
        for error in errors[:100]:
            print(f"- {error}")
        return 1
    print("taxonomy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
