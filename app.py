"""
Financial Analysis Agent - Streamlit Web Interface
Upload CSV files and get instant AI-powered financial analysis
"""

import streamlit as st
import pandas as pd
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Financial Analysis Agent",
    page_icon="📊",
    layout="wide"
)

# Initialize Claude client
client = Anthropic()

# Page title and description
st.title("📊 Financial Analysis Agent")
st.markdown("""
Powered by Claude AI | Analyze financial data instantly

Upload your financial data (CSV) and get AI-powered insights on profitability, 
trends, problems, and recommendations.
""")

# Sidebar for information
st.sidebar.header("📋 About")
st.sidebar.info("""
**Features:**
- 🤖 AI-powered analysis using Claude
- 📈 Automatic trend detection
- 💡 Actionable recommendations
- 📊 Profitability analysis

**How to use:**
1. Upload a CSV file
2. Click "Analyze"
3. Get instant insights!
""")

def analyze_data(data_string):
    """Send financial data to Claude for analysis"""
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": f"""
                You are a financial analysis expert. Analyze this financial data:
                
                {data_string}
                
                Provide analysis in these sections:
                
                ## 🎯 Key Findings
                - Top 3 discoveries with specific numbers
                
                ## 📈 Profitability Analysis
                - Margin trends and calculations
                - Growth patterns
                
                ## ⚠️ Problems & Opportunities
                - 2-3 issues that need attention
                - Growth opportunities
                
                ## 💡 Recommendations
                - 3-5 specific, actionable steps
                - Expected impact
                
                Be concise, specific, and data-driven.
                """
            }
        ]
    )
    return message.content[0].text


# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📤 Upload Your Data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="CSV file with financial data (Month, Revenue, COGS, Profit, etc.)"
    )
    
    if uploaded_file:
        # Read and display the data
        df = pd.read_csv(uploaded_file)
        
        st.subheader("📋 Your Data Preview")
        st.dataframe(df, use_container_width=True)
        
        # Show basic statistics
        st.subheader("📊 Quick Statistics")
        col_a, col_b, col_c = st.columns(3)
        
        if 'Revenue' in df.columns:
            col_a.metric(
                "Total Revenue",
                f"${df['Revenue'].sum():,.0f}"
            )
        
        if 'Profit' in df.columns:
            col_b.metric(
                "Total Profit",
                f"${df['Profit'].sum():,.0f}"
            )
        
        if 'Revenue' in df.columns and 'Profit' in df.columns:
            margin = (df['Profit'].sum() / df['Revenue'].sum() * 100)
            col_c.metric(
                "Profit Margin",
                f"{margin:.1f}%"
            )
        
        # Analyze button
        st.markdown("---")
        
        if st.button("🤖 Analyze with Claude AI", use_container_width=True):
            st.info("Analyzing your data... This may take a few seconds.")
            
            try:
                # Convert data to string for Claude
                data_string = df.to_string()
                
                # Get analysis
                analysis = analyze_data(data_string)
                
                # Display results
                st.success("✅ Analysis complete!")
                
                st.subheader("🔍 AI Analysis Results")
                st.markdown(analysis)
                
                # Download option
                st.download_button(
                    label="📥 Download Analysis",
                    data=analysis,
                    file_name="financial_analysis.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

with col2:
    st.header("📖 Example Data Format")
    
    example_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Revenue': [100000, 105000, 110000, 115000, 120000],
        'COGS': [35000, 36000, 38000, 40000, 42000],
        'Profit': [40000, 44000, 45000, 48000, 51000]
    }
    
    st.dataframe(pd.DataFrame(example_data), use_container_width=True)
    
    st.markdown("""
    **Columns you can use:**
    - Month / Date
    - Revenue
    - COGS (Cost of Goods Sold)
    - Operating Expenses
    - Profit / Net Income
    - Growth %
    """)

# Footer
st.markdown("---")
st.markdown("""
**Built by:** Dhruv Harlalka | **Powered by:** Claude AI | **Tech:** Python, Streamlit, Anthropic API

[GitHub](https://github.com/dhruv-harlalka/dhruv-ai-projects) | 
[LinkedIn](https://linkedin.com/in/dhruv-harlalka)
""")
