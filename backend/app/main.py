from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.portfolio import Portfolio
from app.broker import Broker, Trade, get_historical_prices
from app.simulator import TradingSimulator, all_in_sim

app = FastAPI(title="Nordnet Trading Simulator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
portfolio = Portfolio(initial_cash=100000.0)
broker = Broker()
simulator = TradingSimulator()
simulator.initialize_performance_tracker(100000.0)


@app.get("/")
async def root():
    return {"message": "Nordnet Trading Simulator API"}


@app.get("/portfolio")
async def get_portfolio():
    portfolio_data = portfolio.to_dict()
    total_value = portfolio.get_total_value(broker.get_price)
    
    # Add current prices to positions
    for position in portfolio_data["positions"]:
        current_price = broker.get_price(position["symbol"])
        position["current_price"] = current_price
        position["market_value"] = current_price * position["quantity"]
        position["profit_loss"] = (current_price - position["avg_price"]) * position["quantity"]
        position["profit_loss_pct"] = ((current_price - position["avg_price"]) / position["avg_price"]) * 100
    
    return {
        **portfolio_data,
        "total_value": total_value,
        "total_profit_loss": total_value - 100000.0
    }


@app.post("/trade")
async def execute_trade(trade: Trade):
    # Analyze trade before execution
    current_price = broker.get_price(trade.symbol)
    portfolio_value = portfolio.get_total_value(broker.get_price)
    
    analysis = simulator.analyze_trade(
        trade.action, 
        trade.symbol, 
        trade.quantity, 
        current_price, 
        portfolio_value
    )
    
    # Execute the trade
    result = broker.execute_trade(portfolio, trade)
    
    if "error" in result:
        return result
    
    # Add analysis to result
    result["analysis"] = analysis
    
    return result


@app.get("/history")
async def get_trade_history():
    return {"trades": broker.get_trade_history()}


@app.get("/stock/{symbol}")
async def get_stock_price(symbol: str):
    price = broker.get_price(symbol)
    return {"symbol": symbol, "price": price}


@app.get("/risk")
async def get_risk_metrics():
    positions = portfolio.get_all_positions()
    risk_metrics = simulator.get_risk_metrics(positions, broker.get_price)
    return risk_metrics


@app.get("/performance")
async def get_performance():
    return simulator.get_performance_summary()


@app.get("/historical/{symbol}")
async def get_historical_data(symbol: str, period: str = "1y"):
    """Get historical price data for a symbol."""
    prices = get_historical_prices(symbol, period)
    return {
        "symbol": symbol,
        "period": period,
        "prices": prices,
        "count": len(prices)
    }


@app.get("/simulate/{symbol}")
async def simulate_all_in(symbol: str, period: str = "1y"):
    """Simulate an all-in buy strategy for a symbol."""
    # Get historical prices
    price_history = get_historical_prices(symbol, period)
    
    if not price_history:
        return {
            "error": f"No price data available for {symbol}",
            "symbol": symbol
        }
    
    # Create a fresh portfolio for simulation
    sim_portfolio = Portfolio(cash=10000)
    
    # Run simulation
    portfolio_values = all_in_sim(sim_portfolio, symbol, price_history)
    
    initial_value = 10000
    final_value = portfolio_values[-1] if portfolio_values else initial_value
    total_return = ((final_value - initial_value) / initial_value) * 100
    
    return {
        "symbol": symbol,
        "period": period,
        "initial_cash": initial_value,
        "final_value": round(final_value, 2),
        "total_return_pct": round(total_return, 2),
        "portfolio_values": portfolio_values,
        "data_points": len(portfolio_values)
    }
