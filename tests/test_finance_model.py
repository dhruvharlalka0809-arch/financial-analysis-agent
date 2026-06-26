import unittest

import pandas as pd

from finance_model import build_cfo_memo, normalize_financials, summarize_financials


class FinanceModelTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "Month": ["Jan", "Feb"],
                "Revenue": [100000, 120000],
                "COGS": [40000, 45000],
                "Operating_Expenses": [25000, 26000],
                "Profit": [35000, 49000],
            }
        )

    def test_normalize_financials_calculates_margin_fields(self):
        prepared = normalize_financials(self.df)

        self.assertEqual(prepared.loc[0, "Gross_Profit"], 60000)
        self.assertEqual(prepared.loc[1, "Operating_Profit"], 49000)
        self.assertAlmostEqual(prepared.loc[1, "Reported_Margin"], 49000 / 120000)

    def test_summarize_financials_reconciles_totals(self):
        summary = summarize_financials(self.df)

        self.assertEqual(summary.total_revenue, 220000)
        self.assertEqual(summary.gross_profit, 135000)
        self.assertEqual(summary.operating_profit, 84000)
        self.assertEqual(summary.reported_profit, 84000)
        self.assertAlmostEqual(summary.revenue_growth, 0.2)

    def test_cfo_memo_uses_summary_numbers(self):
        prepared = normalize_financials(self.df)
        summary = summarize_financials(self.df)
        memo = build_cfo_memo(summary, prepared)

        self.assertIn("$220,000", memo)
        self.assertIn("Feb", memo)


if __name__ == "__main__":
    unittest.main()
