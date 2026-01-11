from typing import Dict, List
import random


def all_in_sim(portfolio, symbol, price_history):
    """Simulate an all-in buy strategy with historical prices."""
    if not price_history:
        return []
    start_price = price_history[0]
    quantity = portfolio.cash // start_price
    portfolio.buy(symbol, start_price, quantity)

    values = []
    for price in price_history:
        values.append(portfolio.value({symbol: price}))
    return values


class RiskCalculator:
    @staticmethod
    def calculate_portfolio_risk(positions: List[Dict], get_price_func) -> Dict:
        """Calculate risk metrics for the portfolio."""
        if not positions:
            return {
                "total_value": 0,
                "volatility": 0,
                "diversification_score": 0,
                "risk_level": "low"
            }
        
        total_value = sum(
            pos["quantity"] * get_price_func(pos["symbol"]) 
            for pos in positions
        )
        
        # Mock volatility calculation (in production, use historical data)
        volatility = random.uniform(0.1, 0.3)
        
        # Diversification score based on number of positions
        num_positions = len(positions)
        diversification_score = min(100, num_positions * 20)
        
        # Risk level based on concentration
        max_position_value = max(
            pos["quantity"] * get_price_func(pos["symbol"]) 
            for pos in positions
        )
        concentration = max_position_value / total_value if total_value > 0 else 0
        
        if concentration > 0.5:
            risk_level = "high"
        elif concentration > 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "total_value": total_value,
            "volatility": round(volatility, 3),
            "diversification_score": round(diversification_score, 1),
            "risk_level": risk_level,
            "concentration": round(concentration, 3)
        }


class PerformanceTracker:
    def __init__(self, initial_value: float):
        self.initial_value = initial_value
        self.history: List[Dict] = []
    
    def record_snapshot(self, portfolio_value: float, timestamp: str):
        """Record a portfolio snapshot."""
        return_pct = ((portfolio_value - self.initial_value) / self.initial_value) * 100
        
        self.history.append({
            "timestamp": timestamp,
            "value": portfolio_value,
            "return_pct": round(return_pct, 2)
        })
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary."""
        if not self.history:
            return {
                "total_return": 0,
                "current_value": self.initial_value,
                "initial_value": self.initial_value
            }
        
        latest = self.history[-1]
        return {
            "total_return": latest["return_pct"],
            "current_value": latest["value"],
            "initial_value": self.initial_value,
            "snapshots": len(self.history)
        }


class TradingSimulator:
    def __init__(self):
        self.risk_calculator = RiskCalculator()
        self.performance_tracker = None
    
    def initialize_performance_tracker(self, initial_value: float):
        """Initialize the performance tracker."""
        self.performance_tracker = PerformanceTracker(initial_value)
    
    def analyze_trade(self, trade_type: str, symbol: str, quantity: int, 
                     current_price: float, portfolio_value: float) -> Dict:
        """Analyze a potential trade before execution."""
        trade_value = current_price * quantity
        
        if trade_type == "buy":
            new_position_pct = (trade_value / portfolio_value) * 100 if portfolio_value > 0 else 0
            
            risk_warning = None
            if new_position_pct > 30:
                risk_warning = "This trade will create a concentrated position (>30% of portfolio)"
            
            return {
                "trade_value": trade_value,
                "position_percentage": round(new_position_pct, 2),
                "risk_warning": risk_warning,
                "recommendation": "high_risk" if new_position_pct > 30 else "moderate"
            }
        
        return {
            "trade_value": trade_value,
            "recommendation": "proceed"
        }
    
    def get_risk_metrics(self, positions: List[Dict], get_price_func) -> Dict:
        """Get current risk metrics."""
        return self.risk_calculator.calculate_portfolio_risk(positions, get_price_func)
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary."""
        if not self.performance_tracker:
            return {"error": "Performance tracker not initialized"}
        return self.performance_tracker.get_performance_summary()
