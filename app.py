import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from finance_model import (
    build_ai_prompt,
    build_cfo_memo,
    format_currency,
    format_percent,
    normalize_financials,
    summarize_financials,
)


load_dotenv()

st.set_page_config(
    page_title="FP&A Profitability Intelligence Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    return pd.read_csv("sample_data.csv")


def run_ai_analysis(prepared: pd.DataFrame, summary) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return ""

    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    message = client.messages.create(
        model=model,
        max_tokens=1200,
        messages=[{"role": "user", "content": build_ai_prompt(prepared, summary)}],
    )
    return message.content[0].text


st.title("FP&A Profitability Intelligence Dashboard")
st.caption("P&L analysis, margin leakage, break-even visibility, and CFO-ready recommendations.")

uploaded_file = st.sidebar.file_uploader("Upload financial CSV", type="csv")
st.sidebar.markdown("Use the sample data by default, or upload columns for Revenue, COGS, Operating_Expenses, and Profit.")

try:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file else load_sample_data()
    prepared_df = normalize_financials(raw_df)
    summary = summarize_financials(raw_df)
except Exception as exc:
    st.error(f"Could not analyze the file: {exc}")
    st.stop()

metric_cols = st.columns(4)
metric_cols[0].metric("Revenue", format_currency(summary.total_revenue), format_percent(summary.revenue_growth))
metric_cols[1].metric("Gross Profit", format_currency(summary.gross_profit), format_percent(summary.gross_margin))
metric_cols[2].metric("Reported Profit", format_currency(summary.reported_profit), format_percent(summary.reported_margin))
metric_cols[3].metric("Break-even Revenue", format_currency(summary.break_even_revenue))

st.divider()

trend_tab, margin_tab, memo_tab, data_tab = st.tabs(["P&L Trend", "Margin Drivers", "CFO Memo", "Data"])

with trend_tab:
    st.subheader("Revenue and Profit Trend")
    trend_df = prepared_df.set_index("Month")[["Revenue", "Gross_Profit", "Profit"]]
    st.line_chart(trend_df, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Monthly Profitability")
        st.bar_chart(prepared_df.set_index("Month")[["Gross_Profit", "Operating_Profit", "Profit"]], use_container_width=True)
    with col_b:
        st.markdown("#### Performance Signals")
        st.write(f"Best profit month: **{summary.best_month}**")
        st.write(f"Weakest profit month: **{summary.weakest_month}**")
        st.write(f"Operating margin: **{format_percent(summary.operating_margin)}**")
        st.write(f"Reported profit growth: **{format_percent(summary.reported_profit_growth)}**")

with margin_tab:
    st.subheader("Cost Structure and Margin Leakage")
    cost_df = prepared_df.set_index("Month")[["COGS_Ratio", "Opex_Ratio", "Reported_Margin"]]
    st.line_chart(cost_df, use_container_width=True)

    view_df = prepared_df[
        [
            "Month",
            "Revenue",
            "COGS",
            "Operating_Expenses",
            "Gross_Profit",
            "Operating_Profit",
            "Profit",
            "Reported_Margin",
        ]
    ].copy()
    st.dataframe(
        view_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn("Revenue", format="$%d"),
            "COGS": st.column_config.NumberColumn("COGS", format="$%d"),
            "Operating_Expenses": st.column_config.NumberColumn("Operating Expenses", format="$%d"),
            "Gross_Profit": st.column_config.NumberColumn("Gross Profit", format="$%d"),
            "Operating_Profit": st.column_config.NumberColumn("Operating Profit", format="$%d"),
            "Profit": st.column_config.NumberColumn("Reported Profit", format="$%d"),
            "Reported_Margin": st.column_config.ProgressColumn("Reported Margin", format="%.1f", min_value=0, max_value=1),
        },
    )

with memo_tab:
    st.subheader("Executive Recommendation")
    memo = build_cfo_memo(summary, prepared_df)
    st.markdown(memo)

    if os.getenv("ANTHROPIC_API_KEY"):
        if st.button("Generate AI CFO Analysis"):
            with st.spinner("Building CFO memo..."):
                st.markdown(run_ai_analysis(prepared_df, summary))
    else:
        st.info("Add ANTHROPIC_API_KEY in Streamlit secrets to enable AI-enhanced memo generation.")

    st.download_button(
        "Download memo",
        data=memo,
        file_name="fpa_profitability_memo.md",
        mime="text/markdown",
    )

with data_tab:
    st.subheader("Normalized Financial Model")
    st.dataframe(prepared_df, use_container_width=True, hide_index=True)
