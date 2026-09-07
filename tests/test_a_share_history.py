"""Offline regression tests for A-share history and YTD calculations."""
import ast
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "update_data.py"


class AShareHistoryTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "StockDataManager")
        self.yf = MagicMock()
        self.namespace = {"yf": self.yf, "datetime": SimpleNamespace(now=lambda: datetime(2026, 9, 7))}
        exec(compile(ast.Module(body=[cls], type_ignores=[]), str(SOURCE), "exec"), self.namespace)
        self.manager = self.namespace["StockDataManager"].__new__(self.namespace["StockDataManager"])

    def history(self, dates, prices):
        return pd.DataFrame({"Close": prices}, index=pd.to_datetime(dates))

    def test_preserves_exchange_for_history(self):
        frame = self.history(["2026-09-04"], [100])
        self.yf.Ticker.return_value.history.return_value = frame
        for symbol, expected in [("300308.SZ", "300308.SZ"), ("688041.SS", "688041.SS"), ("600460.SH", "600460.SS")]:
            with self.subTest(symbol=symbol):
                self.assertIs(self.manager.get_a_stock_history(symbol), frame)
                self.yf.Ticker.assert_called_with(expected)

    def test_ytd_uses_previous_year_last_close_not_month_start(self):
        self.yf.Ticker.return_value.history.return_value = self.history(
            ["2025-12-30", "2025-12-31", "2026-01-05", "2026-08-07"], [90, 100, 105, 150])
        self.assertAlmostEqual(self.manager.get_a_stock_ytd_change("300308.SZ", 180), 80)
        self.yf.Ticker.assert_called_with("300308.SZ")
        self.yf.Ticker.return_value.history.assert_called_with(start="2025-12-01")

    def test_ytd_normalizes_sh_alias(self):
        self.yf.Ticker.return_value.history.return_value = self.history(["2025-12-31"], [100])
        self.assertEqual(self.manager.get_a_stock_ytd_change("600460.SH", 90), -10)
        self.yf.Ticker.assert_called_with("600460.SS")

    def test_missing_baseline_is_unavailable(self):
        for frame in [pd.DataFrame(), self.history(["2026-01-05"], [100]),
                      self.history(["2025-12-31"], [0]), self.history(["2025-12-31"], [float("nan")])]:
            with self.subTest(frame=frame):
                self.yf.Ticker.return_value.history.return_value = frame
                self.assertIsNone(self.manager.get_a_stock_ytd_change("300308.SZ", 120))

    def test_source_failure_is_unavailable(self):
        self.yf.Ticker.return_value.history.side_effect = RuntimeError("offline")
        self.assertIsNone(self.manager.get_a_stock_ytd_change("300308.SZ", 120))

    def test_output_formats_missing_ytd_without_dropping_stock(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        expr = next(value for node in ast.walk(tree) if isinstance(node, ast.Dict)
                    for key, value in zip(node.keys, node.values)
                    if isinstance(key, ast.Constant) and key.value == "ytdChange")
        for value, expected in [(None, "--"), (0, "0.00%"), (80, "80.00%")]:
            self.assertEqual(eval(compile(ast.Expression(expr), str(SOURCE), "eval"), {"ytd_change": value}), expected)


if __name__ == "__main__":
    unittest.main()
