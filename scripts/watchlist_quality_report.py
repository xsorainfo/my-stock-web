"""Audit watchlist narrative and taxonomy quality."""

from __future__ import annotations

import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from config import WATCHLIST  # noqa: E402

HEADINGS = ("行业地位", "主营业务", "竞争优势", "未来方向")
PATTERN = re.compile(r"\*\*(行业地位|主营业务|竞争优势|未来方向)\*\*")


def main() -> int:
    duplicates = {}
    issues = []
    for item in WATCHLIST:
        symbol = str(item.get("symbol", "")).strip()
        duplicates[symbol] = duplicates.get(symbol, 0) + 1
        feature = str(item.get("feature") or "")
        found = set(PATTERN.findall(feature))
        missing = [heading for heading in HEADINGS if heading not in found]
        tags = item.get("tags") or []
        if missing:
            issues.append(f"{symbol}: missing headings: {', '.join(missing)}")
        if len(tags) == 0:
            issues.append(f"{symbol}: no tags")
        if len(feature) < 80:
            issues.append(f"{symbol}: feature is too short ({len(feature)} chars)")
        if not item.get("market") and not item.get("market_type"):
            issues.append(f"{symbol}: missing market")
        if not item.get("sector") or not item.get("industry"):
            issues.append(f"{symbol}: missing sector/industry")

    duplicate_symbols = {symbol: count for symbol, count in duplicates.items() if count > 1}
    print(f"watchlist entries: {len(WATCHLIST)}")
    print(f"duplicate symbols: {len(duplicate_symbols)}")
    for symbol, count in sorted(duplicate_symbols.items()):
        print(f"- duplicate: {symbol} ({count})")
    print(f"quality issues: {len(issues)}")
    for issue in issues[:200]:
        print(f"- {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
