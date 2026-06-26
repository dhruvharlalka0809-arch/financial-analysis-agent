# FP&A Profitability Intelligence Dashboard

A Streamlit dashboard that turns monthly P&L data into CFO-ready profitability insight. It combines deterministic financial modeling with optional Claude analysis, so the app works for every reviewer even when no API key is configured.

## What It Does

- Calculates revenue, COGS, gross profit, operating profit, reported profit, margins, growth, and break-even revenue
- Highlights best and weakest profit months from the data
- Visualizes P&L trends, margin movement, and cost structure
- Generates a CFO-style memo with financial readout, risks, and recommended actions
- Optionally enhances the memo with Claude when `ANTHROPIC_API_KEY` is configured

## Why This Project Matters

This is positioned as an FP&A workflow, not a generic chatbot. It shows practical finance judgment, data cleaning, business metric design, Python modeling, Streamlit dashboarding, and responsible AI integration.

## Tech Stack

- Python
- Streamlit
- Pandas
- Anthropic API, optional
- `unittest` validation

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app runs with `sample_data.csv` by default. Upload your own CSV with these columns:

```csv
Month,Revenue,COGS,Operating_Expenses,Profit
January,100000,35000,25000,40000
February,105000,36000,25000,44000
```

## Optional AI Setup

Create a local `.env` file or add Streamlit secrets:

```bash
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_MODEL=claude-sonnet-4-6
```

Do not commit real API keys. `.env`, `.env.*`, `.en`, and Streamlit secrets are ignored by default.

## Validate

```bash
python -m unittest discover -s tests
```

## CLI Mode

```bash
python agent.py sample_data.csv
python agent.py sample_data.csv --ai
```

## Portfolio Talking Points

- Built an FP&A dashboard that reconciles calculations across charts, tables, and memo output
- Converted raw monthly P&L data into decision-ready profitability and break-even metrics
- Designed a fallback memo engine so the product remains usable without paid API access
- Added tests for the core financial model to reduce calculation drift

## Author

Dhruv Harlalka

MBA Finance, Middlesex University Dubai
