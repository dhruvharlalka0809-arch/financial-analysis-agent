# 🤖 Dhruv AI Projects

**AI Agent Portfolio** showcasing financial analysis, market research, sales intelligence, and business operations optimization powered by Claude AI.

---

## 📋 Project 1: Financial Analysis Agent

An intelligent AI agent that analyzes financial data and provides actionable insights.

### ✨ Features

- 📊 **Automatic Financial Analysis** - Analyzes CSV data instantly
- 🤖 **Claude AI Powered** - Uses latest Claude models for deep analysis
- 📈 **Profit Margin Calculations** - Automatic trend detection
- 💡 **Smart Recommendations** - Actionable business insights
- 🎨 **Web Interface** - Beautiful Streamlit dashboard
- 📥 **Download Reports** - Export analysis as text

### 🛠️ Tech Stack

- **Python 3.8+** - Core programming language
- **Claude API** - AI analysis engine
- **Streamlit** - Web interface
- **Pandas** - Data processing
- **python-dotenv** - Environment configuration

---

## 🚀 Quick Start

### Option 1: Live Demo (Easiest)
Visit: [Your Streamlit Link - Coming Soon]

Just upload a CSV and click analyze!

### Option 2: Run Locally

#### Prerequisites
- Python 3.8 or higher
- Claude API key (get it free at https://console.anthropic.com)

#### Installation

```bash
# 1. Clone this repository
git clone https://github.com/dhruv-harlalka/dhruv-ai-projects.git
cd dhruv-ai-projects

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

#### Run the App

```bash
# Option A: Streamlit Web App (Recommended)
streamlit run app.py

# Option B: Command Line Agent
python agent.py
```

---

## 📊 How to Use

### Using the Web App (app.py)

1. Run: `streamlit run app.py`
2. Open: http://localhost:8501
3. Upload a CSV file
4. Click "Analyze with Claude AI"
5. Get instant analysis!

### Using the CLI Agent (agent.py)

1. Run: `python agent.py`
2. Enter CSV file path (or use sample_data.csv)
3. View analysis in terminal

---

## 📁 Input Data Format

Your CSV should have columns like:

```
Month,Revenue,COGS,Operating_Expenses,Profit
January,100000,35000,25000,40000
February,105000,36000,25000,44000
...
```

**Supported columns:**
- `Month` / `Date`
- `Revenue`
- `COGS` (Cost of Goods Sold)
- `Operating_Expenses`
- `Profit` / `Net_Income`
- `Growth_Percentage`

---

## 💡 What the Agent Analyzes

1. **Key Findings** - Top 3 insights with numbers
2. **Profitability Analysis** - Margins, trends, growth
3. **Problems & Opportunities** - Issues and growth potential
4. **Recommendations** - 3-5 specific, actionable steps

---

## 🎯 Output Example

```
## 🎯 Key Findings
- Revenue grew 40% from Jan to Dec
- Average profit margin improved from 40% to 42.86%
- COGS increased by 40% alongside revenue

## 📈 Profitability Analysis
- Consistent month-over-month growth
- Profit margin trending upward
- Operating expenses well-controlled relative to revenue

## ⚠️ Problems & Opportunities
- COGS scaling at same rate as revenue (opportunity to improve efficiency)
- Operating expenses could be optimized
- Strong margin improvement opportunity through cost reduction

## 💡 Recommendations
1. Negotiate supplier contracts to reduce COGS by 5-10%
2. Implement process improvements to reduce operating expenses
3. Scale revenue further while maintaining cost discipline
4. Monitor and analyze high-profit months for patterns
5. Set targets for margin improvement to 45%+
```

---

## 🔐 API Setup

### Get Your Claude API Key

1. Go to: https://console.anthropic.com
2. Sign up (free account)
3. Create API key
4. Add to `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

### Free API Credits
- Free tier includes $5 in monthly credits
- Perfect for testing and learning

---

## 📚 Example Files

- `sample_data.csv` - Example financial data to test with
- `.env.example` - Template for environment setup

---

## 🌟 Portfolio Impact

This project demonstrates:
- ✅ AI/LLM integration skills
- ✅ Python programming expertise
- ✅ Web app development (Streamlit)
- ✅ Data analysis capabilities
- ✅ Problem-solving approach
- ✅ Real business value creation

---

## 🚀 What's Next

Building:
- **Project 2:** Export Market Research Agent
- **Project 3:** Sales Pipeline Intelligence Agent
- **Project 4:** Business Operations Optimizer

---

## 📝 License

MIT License - Feel free to use this project!

---

## 👨‍💻 Author

**Dhruv Harlalka**
- MBA Finance @ Middlesex University Dubai
- AI Enthusiast | Building AI Agents
- 📧 dhruvharlalka0809@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/dhruv-harlalka)
- 🐙 [GitHub](https://github.com/dhruv-harlalka)

---

## 🤝 Support

Questions? Issues? Open an issue on GitHub or reach out!

---

**Built with ❤️ using Claude AI**
