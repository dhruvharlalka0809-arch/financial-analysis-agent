from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = {"Revenue", "COGS", "Operating_Expenses"}


@dataclass(frozen=True)
class FinancialSummary:
    total_revenue: float
    total_cogs: float
    total_operating_expenses: float
    gross_profit: float
    operating_profit: float
    reported_profit: float
    gross_margin: float
    operating_margin: float
    reported_margin: float
    revenue_growth: float
    reported_profit_growth: float
    break_even_revenue: float
    best_month: str
    weakest_month: str


def normalize_financials(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_list}")

    output = df.copy()
    if "Month" not in output.columns:
        output.insert(0, "Month", [f"Period {idx + 1}" for idx in range(len(output))])

    numeric_columns = ["Revenue", "COGS", "Operating_Expenses", "Profit"]
    for column in numeric_columns:
        if column in output.columns:
            output[column] = pd.to_numeric(output[column], errors="coerce").fillna(0)

    output["Gross_Profit"] = output["Revenue"] - output["COGS"]
    output["Operating_Profit"] = output["Gross_Profit"] - output["Operating_Expenses"]
    if "Profit" not in output.columns:
        output["Profit"] = output["Operating_Profit"]

    output["Gross_Margin"] = safe_divide(output["Gross_Profit"], output["Revenue"])
    output["Operating_Margin"] = safe_divide(output["Operating_Profit"], output["Revenue"])
    output["Reported_Margin"] = safe_divide(output["Profit"], output["Revenue"])
    output["COGS_Ratio"] = safe_divide(output["COGS"], output["Revenue"])
    output["Opex_Ratio"] = safe_divide(output["Operating_Expenses"], output["Revenue"])
    output["Revenue_Change"] = output["Revenue"].pct_change().fillna(0)
    output["Profit_Change"] = output["Profit"].pct_change().fillna(0)
    return output


def summarize_financials(df: pd.DataFrame) -> FinancialSummary:
    prepared = normalize_financials(df)
    total_revenue = float(prepared["Revenue"].sum())
    total_cogs = float(prepared["COGS"].sum())
    total_opex = float(prepared["Operating_Expenses"].sum())
    gross_profit = float(prepared["Gross_Profit"].sum())
    operating_profit = float(prepared["Operating_Profit"].sum())
    reported_profit = float(prepared["Profit"].sum())
    gross_margin = divide(gross_profit, total_revenue)
    operating_margin = divide(operating_profit, total_revenue)
    reported_margin = divide(reported_profit, total_revenue)
    revenue_growth = growth_rate(prepared["Revenue"])
    reported_profit_growth = growth_rate(prepared["Profit"])
    contribution_margin = divide(gross_profit, total_revenue)
    break_even_revenue = divide(total_opex, contribution_margin)
    best_month = str(prepared.loc[prepared["Profit"].idxmax(), "Month"])
    weakest_month = str(prepared.loc[prepared["Profit"].idxmin(), "Month"])

    return FinancialSummary(
        total_revenue=total_revenue,
        total_cogs=total_cogs,
        total_operating_expenses=total_opex,
        gross_profit=gross_profit,
        operating_profit=operating_profit,
        reported_profit=reported_profit,
        gross_margin=gross_margin,
        operating_margin=operating_margin,
        reported_margin=reported_margin,
        revenue_growth=revenue_growth,
        reported_profit_growth=reported_profit_growth,
        break_even_revenue=break_even_revenue,
        best_month=best_month,
        weakest_month=weakest_month,
    )


def build_cfo_memo(summary: FinancialSummary, prepared: pd.DataFrame) -> str:
    latest = prepared.iloc[-1]
    strongest_driver = "revenue growth" if summary.revenue_growth >= 0 else "revenue retention"
    margin_signal = "healthy" if summary.reported_margin >= 0.25 else "needs attention"

    return f"""### CFO Memo Draft

**Recommendation:** Keep scaling, but manage cost discipline before the next hiring or expansion decision.

**Financial readout:** Revenue totals {format_currency(summary.total_revenue)} with reported profit of {format_currency(summary.reported_profit)}. Reported margin is {format_percent(summary.reported_margin)}, which is {margin_signal} for a portfolio-stage business.

**Operating signal:** Revenue changed {format_percent(summary.revenue_growth)} from first to last period, while reported profit changed {format_percent(summary.reported_profit_growth)}. The strongest current story is {strongest_driver}, with {summary.best_month} as the best profit month.

**Risk to watch:** Break-even revenue is approximately {format_currency(summary.break_even_revenue)} against latest monthly revenue of {format_currency(float(latest["Revenue"]))}. If COGS or operating expenses rise faster than revenue, the margin story weakens quickly.

**Next action:** Build a monthly budget-vs-actual view and add variance thresholds for COGS, operating expenses, and profit margin.
"""


def build_ai_prompt(prepared: pd.DataFrame, summary: FinancialSummary) -> str:
    return f"""
You are an FP&A analyst writing for a CFO. Analyze the financial table and summary.

Summary:
- Total revenue: {format_currency(summary.total_revenue)}
- Gross profit: {format_currency(summary.gross_profit)}
- Reported profit: {format_currency(summary.reported_profit)}
- Gross margin: {format_percent(summary.gross_margin)}
- Reported margin: {format_percent(summary.reported_margin)}
- Revenue growth: {format_percent(summary.revenue_growth)}
- Profit growth: {format_percent(summary.reported_profit_growth)}
- Break-even revenue: {format_currency(summary.break_even_revenue)}

Data:
{prepared.to_string(index=False)}

Return concise sections:
1. Executive readout
2. Margin and cost drivers
3. Risks
4. Recommended next actions
Use specific numbers from the data.
""".strip()


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value * 100:,.1f}%"


def divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator.div(denominator.replace(0, pd.NA)).fillna(0)


def growth_rate(series: pd.Series) -> float:
    if len(series) < 2:
        return 0.0
    first = float(series.iloc[0])
    last = float(series.iloc[-1])
    return divide(last - first, first)
