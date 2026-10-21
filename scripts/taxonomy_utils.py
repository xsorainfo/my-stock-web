"""Compatibility helpers for the taxonomy migration.

The current data still uses legacy sector/industry/tags fields. These helpers
provide one normalized view without changing the existing data format.
"""

from __future__ import annotations

import re
from typing import Any, Mapping


def first_value(stock: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = stock.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def normalize_taxonomy(stock: Mapping[str, Any]) -> dict[str, Any]:
    """Return normalized taxonomy fields while preserving legacy compatibility."""
    sector_id = first_value(stock, "sector_id", "sector")
    industry_id = first_value(stock, "industry_id", "industry", "industry_code")
    raw_tags = stock.get("tag_ids") or stock.get("tags") or []
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]
    tag_ids = []
    for tag in raw_tags:
        value = str(tag).strip()
        if value and value not in tag_ids:
            tag_ids.append(value)
    theme_ids = stock.get("theme_ids") or stock.get("themes") or []
    if isinstance(theme_ids, str):
        theme_ids = [theme_ids]
    theme_ids = list(dict.fromkeys(str(value).strip() for value in theme_ids if str(value).strip()))
    return {
        "market": first_value(stock, "market", "market_type"),
        "sector_id": sector_id,
        "industry_id": industry_id,
        "theme_ids": theme_ids,
        "tag_ids": tag_ids,
    }


def canonical_key(value: str) -> str:
    """Create a stable lookup key for aliases without changing display text."""
    value = re.sub(r"\\s+", " ", str(value or "").strip().lower())
    return value.replace("（", "(").replace("）", ")")
