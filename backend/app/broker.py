from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel
import yfinance as yf


class Trade(BaseModel):
    symbol: str
    quantity: int
    action: str  # "buy" or "sell"


class TradeRecord(BaseModel):
    symbol: str
    quantity: int
    action: str
    price: float
    timestamp: str
    total_value: float


def get_historical_prices(symbol: str, period="1y"):
    """Get historical closing prices for a symbol."""
    try:
        data = yf.download(symbol, period=period, progress=False)
        return data['Close'].tolist() if 'Close' in data.columns else []
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return []


class Broker:
    def __init__(self):
        self.trade_history: List[Dict] = []
        # Cache for stock prices
        self.prices: Dict[str, float] = {}
    
    def get_price(self, symbol: str) -> float:
        """Get current price for a symbol using yfinance."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Try different price fields in order of preference
            price = (
                info.get('currentPrice') or 
                info.get('regularMarketPrice') or 
                info.get('previousClose')
            )
            
            if price:
                self.prices[symbol] = float(price)
                return float(price)
            
            # Fallback: get latest close from history
            hist = ticker.history(period="1d")
            if not hist.empty and 'Close' in hist.columns:
                price = float(hist['Close'].iloc[-1])
                self.prices[symbol] = price
                return price
                
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
        
        # If all else fails, return cached price or generate mock price
        if symbol in self.prices:
            return self.prices[symbol]
        
        # Generate a pseudo-random price based on symbol as fallback
        base_price = 100.0
        symbol_value = sum(ord(c) for c in symbol)
        fallback_price = base_price + (symbol_value % 200)
        self.prices[symbol] = fallback_price
        return fallback_price
    
    def execute_trade(self, portfolio, trade: Trade) -> Dict:
        """Execute a trade and update portfolio."""
        current_price = self.get_price(trade.symbol)
        total_value = current_price * trade.quantity
        
        if trade.action == "buy":
            if not portfolio.deduct_cash(total_value):
                return {"error": "Insufficient funds"}
            
            portfolio.add_position(trade.symbol, trade.quantity, current_price)
        
        elif trade.action == "sell":
            if not portfolio.remove_position(trade.symbol, trade.quantity):
                if trade.symbol not in portfolio.positions:
                    return {"error": "No position to sell"}
                else:
                    return {"error": "Insufficient shares"}
            
            portfolio.add_cash(total_value)
        
        else:
            return {"error": "Invalid action. Use 'buy' or 'sell'"}
        
        # Record the trade
        trade_record = {
            "symbol": trade.symbol,
            "quantity": trade.quantity,
            "action": trade.action,
            "price": current_price,
            "total_value": total_value,
            "timestamp": datetime.now().isoformat()
        }
        self.trade_history.append(trade_record)
        
        return {"success": True, "trade": trade_record}
    
    def get_trade_history(self) -> List[Dict]:
        """Get all trade history."""
        return self.trade_history
    
    def calculate_commission(self, trade_value: float) -> float:
        """Calculate trading commission (mock implementation)."""
        # Example: 0.1% commission with minimum $1
        commission = max(1.0, trade_value * 0.001)
        return commission
