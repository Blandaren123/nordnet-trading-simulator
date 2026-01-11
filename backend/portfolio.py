"""
Portfolio Tracker Module
Tracks portfolio performance, holdings, and returns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class Portfolio:
    """Portfolio tracker for managing investments and calculating performance"""
    
    def __init__(self, initial_cash: float = 100000.0):
        """
        Initialize portfolio with starting cash
        
        Args:
            initial_cash: Starting cash amount in SEK
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.holdings: Dict[str, float] = {}  # symbol -> quantity
        self.transactions: List[Dict] = []
        self.purchase_prices: Dict[str, List[Dict]] = {}  # symbol -> [{price, quantity, date}]
        
    def buy(self, symbol: str, quantity: float, price: float, date: Optional[datetime] = None) -> bool:
        """
        Buy shares of a stock
        
        Args:
            symbol: Stock ticker symbol
            quantity: Number of shares to buy
            price: Price per share
            date: Transaction date (defaults to now)
            
        Returns:
            True if successful, False if insufficient funds
        """
        if date is None:
            date = datetime.now()
            
        cost = quantity * price
        if cost > self.cash:
            return False
            
        self.cash -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        
        # Track purchase price for calculating gains
        if symbol not in self.purchase_prices:
            self.purchase_prices[symbol] = []
        self.purchase_prices[symbol].append({
            'price': price,
            'quantity': quantity,
            'date': date
        })
        
        self.transactions.append({
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'date': date,
            'total': cost
        })
        
        return True
    
    def sell(self, symbol: str, quantity: float, price: float, date: Optional[datetime] = None) -> bool:
        """
        Sell shares of a stock
        
        Args:
            symbol: Stock ticker symbol
            quantity: Number of shares to sell
            price: Price per share
            date: Transaction date (defaults to now)
            
        Returns:
            True if successful, False if insufficient holdings
        """
        if date is None:
            date = datetime.now()
            
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
            
        proceeds = quantity * price
        self.cash += proceeds
        self.holdings[symbol] -= quantity
        
        # Remove from holdings if quantity reaches 0
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transactions.append({
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'date': date,
            'total': proceeds
        })
        
        return True
    
    def get_position_value(self, symbol: str, current_price: float) -> float:
        """Calculate current value of a position"""
        if symbol not in self.holdings:
            return 0.0
        return self.holdings[symbol] * current_price
    
    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value
        
        Args:
            current_prices: Dict of symbol -> current price
            
        Returns:
            Total portfolio value including cash
        """
        holdings_value = sum(
            self.get_position_value(symbol, current_prices.get(symbol, 0))
            for symbol in self.holdings
        )
        return self.cash + holdings_value
    
    def get_return(self, current_prices: Dict[str, float]) -> float:
        """
        Calculate total return percentage
        
        Args:
            current_prices: Dict of symbol -> current price
            
        Returns:
            Return as percentage
        """
        current_value = self.get_total_value(current_prices)
        return ((current_value - self.initial_cash) / self.initial_cash) * 100
    
    def get_position_gains(self, symbol: str, current_price: float) -> Dict:
        """
        Calculate gains/losses for a specific position
        
        Args:
            symbol: Stock ticker symbol
            current_price: Current price per share
            
        Returns:
            Dict with gain amount and percentage
        """
        if symbol not in self.holdings or symbol not in self.purchase_prices:
            return {'gain': 0, 'gain_pct': 0}
        
        # Calculate average purchase price
        total_cost = sum(p['price'] * p['quantity'] for p in self.purchase_prices[symbol])
        total_quantity = sum(p['quantity'] for p in self.purchase_prices[symbol])
        avg_price = total_cost / total_quantity if total_quantity > 0 else 0
        
        current_value = self.holdings[symbol] * current_price
        cost_basis = self.holdings[symbol] * avg_price
        
        gain = current_value - cost_basis
        gain_pct = (gain / cost_basis * 100) if cost_basis > 0 else 0
        
        return {
            'gain': gain,
            'gain_pct': gain_pct,
            'avg_price': avg_price,
            'current_price': current_price
        }
    
    def get_summary(self, current_prices: Dict[str, float]) -> Dict:
        """
        Get portfolio summary
        
        Args:
            current_prices: Dict of symbol -> current price
            
        Returns:
            Dict with portfolio summary statistics
        """
        total_value = self.get_total_value(current_prices)
        total_return = self.get_return(current_prices)
        
        positions = {}
        for symbol in self.holdings:
            current_price = current_prices.get(symbol, 0)
            position_value = self.get_position_value(symbol, current_price)
            gains = self.get_position_gains(symbol, current_price)
            
            positions[symbol] = {
                'quantity': self.holdings[symbol],
                'current_price': current_price,
                'value': position_value,
                'weight': (position_value / total_value * 100) if total_value > 0 else 0,
                'avg_price': gains['avg_price'],
                'gain': gains['gain'],
                'gain_pct': gains['gain_pct']
            }
        
        return {
            'total_value': total_value,
            'cash': self.cash,
            'invested_value': total_value - self.cash,
            'initial_cash': self.initial_cash,
            'total_return': total_return,
            'total_gain': total_value - self.initial_cash,
            'positions': positions,
            'num_positions': len(self.holdings),
            'num_transactions': len(self.transactions)
        }
    
    def get_transaction_history(self) -> pd.DataFrame:
        """Get transaction history as DataFrame"""
        if not self.transactions:
            return pd.DataFrame()
        return pd.DataFrame(self.transactions)
