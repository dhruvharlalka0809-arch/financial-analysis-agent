"""
Financial Analysis Agent
Analyzes financial data using Claude AI
"""

import pandas as pd
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Claude client
client = Anthropic()

def analyze_financial_data(csv_file_path):
    """
    Financial Analysis Agent that takes CSV data and analyzes it using Claude
    
    Args:
        csv_file_path: Path to CSV file with financial data
        
    Returns:
        Claude's analysis as a string
    """
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Convert to string for Claude to analyze
        data_string = df.to_string()
        
        # Send to Claude for analysis
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You are a financial analysis expert. Analyze this financial data and provide detailed insights:
                    
                    {data_string}
                    
                    Please provide:
                    1. **Top 3 Key Findings** - What stands out most?
                    2. **Profitability Analysis** - Calculate margins, trends
                    3. **Problems & Opportunities** - What needs attention?
                    4. **Specific Recommendations** - 3-5 actionable steps
                    
                    Be concise, specific, and use numbers. Format as clear sections.
                    """
                }
            ]
        )
        
        return message.content[0].text
    
    except FileNotFoundError:
        return f"Error: File '{csv_file_path}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main function to run the agent"""
    print("=" * 60)
    print("💰 FINANCIAL ANALYSIS AGENT")
    print("=" * 60)
    print("\nThis agent analyzes financial data using Claude AI\n")
    
    # Get CSV file path from user
    csv_file = input("Enter CSV file path (or press Enter for sample_data.csv): ").strip()
    
    if not csv_file:
        csv_file = "sample_data.csv"
    
    print(f"\n🔍 Analyzing {csv_file}...")
    print("-" * 60)
    
    # Analyze the data
    analysis = analyze_financial_data(csv_file)
    
    print("\n📊 ANALYSIS RESULTS:\n")
    print(analysis)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
