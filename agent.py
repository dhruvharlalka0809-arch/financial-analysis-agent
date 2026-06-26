import os
import sys

import pandas as pd
from dotenv import load_dotenv

from finance_model import build_ai_prompt, build_cfo_memo, normalize_financials, summarize_financials


load_dotenv()


def analyze_financial_data(csv_file_path: str, use_ai: bool = False) -> str:
    df = pd.read_csv(csv_file_path)
    prepared = normalize_financials(df)
    summary = summarize_financials(df)

    if not use_ai or not os.getenv("ANTHROPIC_API_KEY"):
        return build_cfo_memo(summary, prepared)

    from anthropic import Anthropic

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    message = client.messages.create(
        model=model,
        max_tokens=1200,
        messages=[{"role": "user", "content": build_ai_prompt(prepared, summary)}],
    )
    return message.content[0].text


def main() -> None:
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "sample_data.csv"
    use_ai = "--ai" in sys.argv
    print(analyze_financial_data(csv_file, use_ai=use_ai))


if __name__ == "__main__":
    main()
