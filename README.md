# 📊 Market Seasonality Analysis Tool by Nicola Chimenti

A comprehensive **web-based seasonality analyzer** built with **Streamlit** and **Python**, designed to uncover seasonal patterns in financial markets, backtest simple strategies, and provide detailed statistical analysis.  
This tool helps traders and analysts identify market tendencies, develop data-driven strategies, and make informed trading decisions based on historical patterns.

## 🌐 Live Demo

**Try it now:** [web app link](https://seasonalityanalysis.streamlit.app/)
No installation required — start analyzing market seasonality immediately in your browser!

---

## 🧩 Features

### 📈 Comprehensive Market Analysis
Deep dive into historical market behavior with month-by-month analysis:
- **Monthly return patterns** across multiple years
- **Win rate statistics** for each month
- **High/Low excursions** tracking
- **Standard deviation** and volatility metrics
- **Interactive and static** visualization modes

**Key Capabilities:**
- Yahoo Finance API integration for reliable data
- Customizable time periods (from 1850 to present)
- Support for any ticker available on Yahoo Finance
- Real-time data validation and error handling
- Mobile-responsive interface with alternative chart modes

---

### 💡 Strategy Development & Backtesting
Create and test simple seasonal trading strategies:
- **1-month holding period** strategy testing
- **Entry/Exit optimization** based on seasonal patterns
- **Performance metrics** including:
  - Win Rate and Average Returns
  - Profit Factor
  - Sortino Ratio (with/without benchmark)
  - Maximum Drawdown
  - Calmar Ratio

**Strategy Features:**
- Benchmark comparison (default: S&P 500)
- Historical drawdown tracking
- Risk-adjusted performance metrics
- Visual performance representation

---

### 📊 Advanced Visualization
Multiple chart types for comprehensive analysis:
- **Bar charts** showing yearly returns by month
- **Standard deviation bands** for volatility assessment
- **Interactive Altair charts** with hover details
- **Static Matplotlib charts** for presentations
- **Win rate comparison** charts
- **Color-coded performance** indicators

**Display Options:**
- Choose between interactive and image-based charts
- Customizable data representation
- Export-ready database views
- CSV-compatible formatting

---

### 🎯 Multi-Language Support
Professional interface in:
- 🇬🇧 **English**
- 🇮🇹 **Italiano** *(coming soon)*
- 🇷🇺 **Русский** *(coming soon)*

---

## 📦 Local Installation

If you prefer to run it locally or modify the code:

#### Prerequisites
- Python 3.8 or higher
- pip package manager

#### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/TeknoTrader/SEASONALITY.git
cd SEASONALITY
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run WebApp.py
```

4. **Open your browser**  
The app will automatically open at `http://localhost:8501`

---

## 🚀 Usage

### Analysis Mode

1. **Navigate to the "Analysis" page**
2. **Enter parameters**:
   - Starting year (minimum 1850)
   - Ending year (up to current year)
   - Ticker symbol (e.g., GOOG, AAPL, ^GSPC)
3. **Select output options**:
   - Choose specific months or analyze all 12
   - Select chart type (Interactive/Image)
   - Choose database format (User Friendly/CSV)
4. **Review results**:
   - Monthly performance statistics
   - Visual charts with standard deviation bands
   - Detailed year-by-year data tables

### Strategy Mode

1. **Navigate to the "Basic Strategy" page**
2. **Configure strategy**:
   - Set time period
   - Select ticker
   - Choose months to trade
   - Enable/disable benchmark comparison
3. **Click "Ready to go!"** to calculate
4. **Analyze performance**:
   - Overall strategy metrics
   - Month-by-month breakdown
   - Risk-adjusted returns
   - Drawdown analysis

---

## 📁 Project Structure

```
SEASONALITY/
├── WebApp.py              # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔧 Technical Details

**Built with:**
- **Streamlit**: Modern web framework for data apps
- **yfinance**: Yahoo Finance API wrapper for market data
- **Altair**: Declarative statistical visualizations
- **Matplotlib**: Static chart generation
- **Pandas & NumPy**: Data manipulation and statistical analysis
- **python-dateutil**: Advanced date handling

**Performance Metrics:**
- **Win Rate**: Percentage of profitable periods
- **Profit Factor**: Ratio of gross profit to gross loss
- **Sortino Ratio**: Risk-adjusted return focusing on downside deviation
- **Calmar Ratio**: Return vs. maximum drawdown
- **Maximum Drawdown**: Largest peak-to-trough decline

**Data Source:**
- Yahoo Finance API via yfinance library
- Historical data availability varies by asset
- Monthly interval data for accurate seasonal analysis

---

## 💼 Use Cases

This tool is perfect for:
- **Quantitative Traders** developing seasonal trading strategies
- **Portfolio Managers** timing market entry/exit points
- **Financial Analysts** identifying market patterns and anomalies
- **Students & Researchers** studying market behavior and seasonality
- **Algorithmic Traders** backtesting calendar-based strategies
- **Risk Managers** assessing seasonal risk patterns

---

## 🎯 Roadmap

Future enhancements planned:
- [ ] Multi-asset portfolio seasonality analysis
- [ ] Advanced strategy builder with multiple entry/exit rules
- [ ] Machine learning pattern recognition
- [ ] Sector rotation analysis
- [ ] Correlation matrix for seasonal patterns
- [ ] PDF report generation
- [ ] More sophisticated risk metrics
- [ ] Real-time alert system for seasonal opportunities
- [ ] Integration with broker APIs for live trading

---

## 📊 Example Analysis

**Scenario:** Analyzing GOOG (Google) from 2010 to 2024

**Findings:**
- September shows historically negative bias (-2.3% average)
- Win Rate: 42% (below 50% threshold)
- April demonstrates strong positive tendency (+3.1% average)
- Win Rate: 71% (above 60% threshold)
- Standard Deviation: 4.2% (moderate volatility)

**Strategy Implication:**
- Consider avoiding long positions in September
- Favor long positions in April
- Use tighter stop-losses during high-volatility months

---

## ⚠️ Risk Disclaimer

**IMPORTANT**: This tool is for educational and research purposes only.

**Key Considerations:**
1. **Past performance does not guarantee future results**
2. **Market conditions change** - Historical patterns may not repeat
3. **Statistical significance** - Ensure adequate sample size
4. **Overfitting risk** - Avoid excessive optimization on historical data
5. **Out-of-sample testing** - Always validate on unseen data
6. **Risk management** - Position sizing and stop-losses are crucial
7. **Market dynamics** - Structural changes can invalidate patterns

**Before trading:**
- Thoroughly understand the risks involved
- Never risk more than you can afford to lose
- Consider consulting with a financial advisor
- Implement proper risk management techniques
- Use out-of-sample validation periods

---

## 💬 Feedback & Contributions

If you find this tool useful or have ideas for improvement, feel free to:
- Open an **[Issue](../../issues)** for bug reports or feature requests
- Submit a **Pull Request** to contribute enhancements
- Share your findings and use cases
- Suggest new metrics or analysis methods

Community feedback drives development!

---

## 📜 License

Distributed under the **MIT License** — free to use, modify, and share with proper attribution.

---

## 👤 Author

**Nicola Chimenti**  
Quantitative Trading Enthusiast & Financial Software Developer

🎓 Student of Digital Economics  
💼 Trading Software Developer specializing in strategy automation

🌐 [MQL5 Profile](https://www.mql5.com/it/users/teknotrader/seller#!category=2)  
🔗 [LinkedIn](https://www.linkedin.com/in/nicolachimenti)  
💻 [GitHub](https://github.com/TeknoTrader)  
📧 Email: nicola.chimenti.work@gmail.com

---

## 🙏 Acknowledgments

This project was developed to help traders and analysts make more informed decisions by leveraging historical market patterns. The goal is to provide a transparent, data-driven approach to understanding market seasonality.

**Special Thanks:**
- Yahoo Finance for providing free market data API
- The Streamlit community for excellent documentation
- Traders who provided feedback and suggestions

---

## ❓ FAQ

**Q: Can I use this for live trading?**  
A: This tool is designed for research and backtesting. Live trading requires additional considerations like execution costs, slippage, and real-time risk management.

**Q: How accurate is the data?**  
A: Data comes directly from Yahoo Finance. While generally reliable, always verify critical data points independently.

**Q: Can I analyze cryptocurrencies?**  
A: Yes! Any asset with a Yahoo Finance ticker can be analyzed (e.g., BTC-USD, ETH-USD).

**Q: What's the minimum historical period needed?**  
A: For reliable statistical analysis, aim for at least 10-15 years of data. More is better.

**Q: Can I export the analysis?**  
A: Yes, select "For CSV download" in the database representation options to get export-ready formatted data.

**Q: Does it work with forex pairs?**  
A: Yes, if the forex pair has a Yahoo Finance ticker (e.g., EURUSD=X).

**Q: What's the difference between Sortino and Sharpe Ratio?**  
A: Sortino focuses only on downside volatility, while Sharpe considers all volatility. Sortino is often preferred for asymmetric return distributions.

**Q: Can I analyze intraday patterns?**  
A: Currently, the tool focuses on monthly seasonality. Intraday analysis may be added in future versions.

---

## 📚 Methodology

### Statistical Approach
The tool uses rigorous statistical methods:
- **Sample size validation** to ensure significance
- **Standard deviation** for volatility measurement
- **Z-scores** for outlier identification
- **Historical simulation** for realistic backtesting

### Performance Metrics Explained

**Win Rate**: Percentage of profitable months
- Above 60%: Strong positive bias
- 40-60%: Neutral bias
- Below 40%: Negative bias

**Profit Factor**: Total profits / Total losses
- Above 2.0: Excellent
- 1.5-2.0: Good
- 1.0-1.5: Acceptable
- Below 1.0: Losing strategy

**Sortino Ratio**: (Return - Risk-free rate) / Downside deviation
- Above 2.0: Excellent risk-adjusted returns
- 1.0-2.0: Good
- Below 1.0: Poor risk-adjusted returns

---

⭐ **If you find this tool helpful, please give the repository a star — it helps others discover it!**

---

**VAT Code**: 02674000464  
**Company**: Tekno Trader  
**© 2024 Nicola Chimenti. All rights reserved.**
