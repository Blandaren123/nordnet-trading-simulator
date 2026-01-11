# Nordnet Trading Simulator 📈

A comprehensive trading and investing tool with portfolio tracking, backtesting, risk analysis, and scenario simulation capabilities.

## Features

### 🎯 Core Features

1. **Portfolio Tracker**
   - Track your investments in real-time
   - Monitor performance and returns
   - View detailed position analytics
   - Transaction history tracking

2. **Backtesting Simulator**
   - Test trading strategies on historical data
   - Buy-and-Hold strategy
   - SMA Crossover strategy (50/200)
   - Performance metrics (Sharpe ratio, max drawdown)
   - Visual equity curves

3. **Risk/Reward Calculator**
   - Calculate optimal position sizes
   - Risk/reward ratio analysis
   - Value at Risk (VaR) calculations
   - Portfolio volatility metrics
   - Kelly Criterion position sizing

4. **Stop Loss / Take Profit Simulator**
   - Simulate trades with SL/TP levels
   - Optimize exit strategies
   - Multiple trade backtesting
   - Performance analysis

5. **What-If Simulator** 🚀
   - "What if I all-in RXRX / IonQ?" scenarios
   - Compare multiple stocks
   - Dollar-Cost Averaging vs Lump Sum
   - Extreme scenario testing

## Tech Stack

### Backend
- **Python 3.x** with modern async capabilities
- **Pandas** for data manipulation and analysis
- **NumPy** for numerical computations
- **yfinance** for historical stock data
- **Flask** for REST API
- **Flask-CORS** for cross-origin requests

### Frontend
- **React** for UI components
- **React Router** for navigation
- **Recharts** for data visualization
- **Axios** for API calls
- **CSS3** with modern gradients and animations

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Blandaren123/nordnet-trading-simulator.git
cd nordnet-trading-simulator
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python -m backend.api
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Usage

### Portfolio Tracker

1. Create a portfolio with initial cash (default: 100,000 SEK)
2. Buy stocks by entering symbol, quantity, and price
3. Sell stocks from your holdings
4. View real-time portfolio performance

### Backtesting

1. Enter stock symbol (e.g., AAPL, TSLA)
2. Select date range
3. Choose strategy (Buy-and-Hold or SMA Crossover)
4. Run backtest and analyze results

### Risk Calculator

1. **Position Size Calculator**: Calculate how many shares to buy based on your risk tolerance
2. **Risk/Reward Calculator**: Determine if a trade setup has favorable risk/reward ratio

### Stop Loss/Take Profit Simulator

1. Set entry price and position size
2. Define stop loss and take profit percentages
3. Simulate trade outcome based on historical data
4. Optimize SL/TP levels for best results

### What-If Simulator

1. **Single Stock**: Enter symbol and investment amount to see historical performance
2. **Compare Stocks**: Enter multiple symbols to compare performance
3. **DCA Analysis**: Compare lump sum vs dollar-cost averaging strategies

## API Endpoints

### Portfolio
- `POST /api/portfolio/create` - Create new portfolio
- `POST /api/portfolio/{id}/buy` - Execute buy order
- `POST /api/portfolio/{id}/sell` - Execute sell order
- `GET /api/portfolio/{id}/summary` - Get portfolio summary
- `GET /api/portfolio/{id}/transactions` - Get transaction history

### Data
- `GET /api/data/historical` - Get historical price data
- `GET /api/data/price` - Get current price
- `GET /api/data/info` - Get stock information

### Backtesting
- `POST /api/backtest/buy-hold` - Run buy-and-hold backtest
- `POST /api/backtest/sma-crossover` - Run SMA crossover backtest

### Risk Analysis
- `POST /api/risk/position-size` - Calculate position size
- `POST /api/risk/risk-reward` - Calculate risk/reward ratio

### Stop Loss/Take Profit
- `POST /api/sltp/simulate` - Simulate single trade
- `POST /api/sltp/optimize` - Optimize SL/TP levels

### What-If Scenarios
- `POST /api/whatif/all-in` - Simulate all-in scenario
- `POST /api/whatif/compare` - Compare multiple scenarios
- `POST /api/whatif/dca` - Dollar-cost averaging simulation
- `POST /api/whatif/lump-vs-dca` - Compare lump sum vs DCA

## Example Scenarios

### Example 1: "What if I all-in IONQ?"
```python
# Simulate investing 100,000 SEK in IONQ from 2024-01-01 to today
{
  "symbol": "IONQ",
  "investment_amount": 100000,
  "start_date": "2024-01-01"
}
```

### Example 2: Compare RXRX vs IONQ
```python
# Compare performance of multiple stocks
{
  "symbols": ["RXRX", "IONQ", "AAPL"],
  "investment_amount": 100000,
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

### Example 3: Optimize Stop Loss/Take Profit
```python
# Find optimal SL/TP levels for a stock
{
  "symbol": "TSLA",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

## Risk Disclaimer

⚠️ **Important**: This simulator is for **educational and entertainment purposes only**. 

- Past performance does not guarantee future results
- Going "all-in" on any single stock is extremely risky
- Always diversify your portfolio
- Never invest more than you can afford to lose
- Consult with a financial advisor before making investment decisions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for learning and development.

## Author

Built with ❤️ for traders and investors who want to test their strategies before risking real money.

---

**Happy Trading! 🚀📊**

