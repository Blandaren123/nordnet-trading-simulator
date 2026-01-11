from typing import Dict, List, Optional
from pydantic import BaseModel


class Position(BaseModel):
    symbol: str
    quantity: int
    avg_price: float


class Portfolio:
    def __init__(self, cash=10000):
        self.cash = cash
        self.holdings = {}

    def buy(self, symbol, price, quantity):
        cost = price * quantity
        if self.cash >= cost:
            self.cash -= cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity

    def value(self, current_prices):
        total = self.cash
        for sym, qty in self.holdings.items():
            total += current_prices.get(sym, 0) * qty
        return total
    
    # Keep compatibility with existing code
    def get_position(self, symbol: str) -> Optional[Dict]:
        if symbol in self.holdings:
            return {"quantity": self.holdings[symbol], "avg_price": 0}
        return None
    
    def get_all_positions(self) -> List[Dict]:
        return [
            {
                "symbol": symbol,
                "quantity": qty,
                "avg_price": 0
            }
            for symbol, qty in self.holdings.items()
        ]
    
    def add_position(self, symbol: str, quantity: int, price: float):
        self.buy(symbol, price, quantity)
    
    def remove_position(self, symbol: str, quantity: int) -> bool:
        if symbol not in self.holdings:
            return False
        
        if self.holdings[symbol] < quantity:
            return False
        
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        return True
    
    def deduct_cash(self, amount: float) -> bool:
        if self.cash < amount:
            return False
        self.cash -= amount
        return True
    
    def add_cash(self, amount: float):
        self.cash += amount
    
    def get_total_value(self, get_price_func) -> float:
        current_prices = {}
        for symbol in self.holdings.keys():
            current_prices[symbol] = get_price_func(symbol)
        return self.value(current_prices)
    
    def to_dict(self) -> Dict:
        return {
            "cash": self.cash,
            "positions": self.get_all_positions()
        }
