# Quick Start Guide

## Installation & Setup

### 1. Install Dependencies

**Backend (Python):**
```bash
pip install -r requirements.txt
```

**Frontend (React):**
```bash
cd frontend
npm install
```

### 2. Start the Application

**Option A: Using the startup script (recommended)**
```bash
./start.sh
```

**Option B: Manual start**

Terminal 1 - Backend:
```bash
python -m backend.api
```

Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

The application will open at `http://localhost:3000`

## Quick Demo

Run the demo script to see the backend in action:
```bash
python demo.py
```

## Testing Individual Features

### 1. Portfolio Tracker
- Navigate to Portfolio tab
- Click "Create Portfolio" (100,000 SEK default)
- Add trades: Enter symbol (e.g., AAPL), quantity, and price
- Click "Buy" or "Sell"
- View your positions and performance

### 2. Backtesting
- Navigate to Backtesting tab
- Enter a stock symbol (e.g., AAPL, TSLA)
- Select date range (e.g., 2023-01-01 to 2024-01-01)
- Choose strategy: Buy-and-Hold or SMA Crossover
- Click "Run Backtest"
- View results with equity curve chart

### 3. Risk Calculator
- Navigate to Risk Calculator tab
- **Position Size**: Enter account value, risk %, entry price, stop loss
- **Risk/Reward**: Enter entry, stop loss, and take profit prices
- View calculated recommendations

### 4. Stop Loss/Take Profit Simulator
- Navigate to Stop Loss/TP tab
- Enter symbol, entry price, quantity
- Set stop loss % and take profit %
- Select date range
- Click "Simulate Trade" or "Optimize SL/TP Levels"

### 5. What-If Simulator
- Navigate to What-If Simulator tab
- **Single Stock**: Enter symbol (e.g., RXRX, IONQ), amount, and dates
- **Compare**: Enter multiple symbols separated by commas
- View detailed results with charts

## Example Scenarios

### Example 1: "What if I all-in IONQ?"
1. Go to What-If Simulator
2. Enter: Symbol = IONQ, Amount = 100000, Start Date = 2024-01-01
3. Click "Simulate All-In Scenario"
4. View: Returns, drawdowns, volatility, timeline chart

### Example 2: Optimize Trading Strategy
1. Go to Stop Loss/TP Simulator
2. Enter: Symbol = AAPL, dates from 2024-01-01 to 2024-12-31
3. Click "Optimize SL/TP Levels"
4. View best stop loss and take profit percentages

### Example 3: Backtest SMA Strategy
1. Go to Backtesting
2. Enter: Symbol = TSLA, dates, strategy = SMA Crossover
3. Click "Run Backtest"
4. Compare Sharpe ratio and max drawdown

## API Testing with curl

### Get Current Price
```bash
curl "http://localhost:5000/api/data/price?symbol=AAPL"
```

### Create Portfolio
```bash
curl -X POST http://localhost:5000/api/portfolio/create \
  -H "Content-Type: application/json" \
  -d '{"portfolio_id": "test", "initial_cash": 100000}'
```

### Run Backtest
```bash
curl -X POST http://localhost:5000/api/backtest/buy-hold \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01",
    "initial_cash": 100000
  }'
```

### What-If Scenario
```bash
curl -X POST http://localhost:5000/api/whatif/all-in \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "RXRX",
    "investment_amount": 100000,
    "start_date": "2024-01-01"
  }'
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.x is installed: `python3 --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

### Frontend won't start
- Ensure Node.js is installed: `node --version`
- Install dependencies: `cd frontend && npm install`
- Check port 3000 is available

### API errors
- Ensure backend is running on port 5000
- Check CORS settings if accessing from different domain
- Verify internet connection for fetching stock data

### No stock data
- Stock symbols must be valid Yahoo Finance tickers
- Some stocks may not have historical data for all date ranges
- Check internet connection

## Next Steps

1. Explore all features in the UI
2. Try different stocks and date ranges
3. Compare multiple what-if scenarios
4. Optimize your trading strategies
5. Use the risk calculator before every trade!

## Support

For issues or questions, please create an issue on the GitHub repository.

**Remember**: This is for educational purposes only. Past performance does not guarantee future results!
