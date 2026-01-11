"""
Backtesting Module
Simulates trading strategies on historical data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Callable
from .portfolio import Portfolio
from .data_fetcher import DataFetcher


class Backtester:
    """Backtest trading strategies on historical data"""
    
    def __init__(self, initial_cash: float = 100000.0):
        """
        Initialize backtester
        
        Args:
            initial_cash: Starting cash amount
        """
        self.initial_cash = initial_cash
        self.portfolio = Portfolio(initial_cash)
        self.equity_curve: List[Dict] = []
        
    def run_buy_and_hold(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        allocation: float = 1.0
    ) -> Dict:
        """
        Backtest buy and hold strategy
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            allocation: Portion of cash to invest (0.0 to 1.0)
            
        Returns:
            Dict with backtest results
        """
        # Fetch historical data
        df = DataFetcher.get_historical_data(symbol, start_date, end_date)
        
        if df.empty:
            return {'error': 'No data available for specified period'}
        
        # Buy at the first available price
        first_price = float(df['Close'].iloc[0])
        first_date = df.index[0].to_pydatetime()
        
        invest_amount = self.initial_cash * allocation
        quantity = invest_amount / first_price
        
        success = self.portfolio.buy(symbol, quantity, first_price, first_date)
        
        if not success:
            return {'error': 'Failed to execute buy order'}
        
        # Track equity curve
        for date, row in df.iterrows():
            current_price = float(row['Close'])
            total_value = self.portfolio.get_total_value({symbol: current_price})
            
            self.equity_curve.append({
                'date': date.to_pydatetime(),
                'value': total_value,
                'price': current_price
            })
        
        # Calculate final results
        final_price = float(df['Close'].iloc[-1])
        final_value = self.portfolio.get_total_value({symbol: final_price})
        total_return = ((final_value - self.initial_cash) / self.initial_cash) * 100
        
        # Calculate metrics
        df_equity = pd.DataFrame(self.equity_curve)
        df_equity['returns'] = df_equity['value'].pct_change()
        
        sharpe_ratio = self._calculate_sharpe_ratio(df_equity['returns'].dropna())
        max_drawdown = self._calculate_max_drawdown(df_equity['value'])
        
        return {
            'strategy': 'Buy and Hold',
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'initial_value': self.initial_cash,
            'final_value': final_value,
            'total_return': total_return,
            'buy_price': first_price,
            'sell_price': final_price,
            'quantity': quantity,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'equity_curve': self.equity_curve,
            'num_trades': 1
        }
    
    def run_sma_crossover(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        short_window: int = 50,
        long_window: int = 200,
        allocation: float = 1.0
    ) -> Dict:
        """
        Backtest SMA crossover strategy
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            short_window: Short SMA period
            long_window: Long SMA period
            allocation: Portion of cash to use per trade
            
        Returns:
            Dict with backtest results
        """
        # Fetch historical data
        df = DataFetcher.get_historical_data(symbol, start_date, end_date)
        
        if df.empty or len(df) < long_window:
            return {'error': 'Insufficient data for strategy'}
        
        # Calculate SMAs
        df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=long_window).mean()
        
        # Generate signals
        df['Signal'] = 0
        df.loc[df['SMA_short'] > df['SMA_long'], 'Signal'] = 1  # Buy signal
        df['Position'] = df['Signal'].diff()
        
        # Simulate trading
        position = 0
        num_trades = 0
        
        for date, row in df.iterrows():
            if pd.isna(row['Position']):
                continue
                
            current_price = float(row['Close'])
            current_date = date.to_pydatetime()
            
            # Buy signal (crossover up)
            if row['Position'] == 1 and position == 0:
                invest_amount = self.portfolio.cash * allocation
                quantity = invest_amount / current_price
                if self.portfolio.buy(symbol, quantity, current_price, current_date):
                    position = quantity
                    num_trades += 1
            
            # Sell signal (crossover down)
            elif row['Position'] == -1 and position > 0:
                if self.portfolio.sell(symbol, position, current_price, current_date):
                    position = 0
                    num_trades += 1
            
            # Track equity curve
            current_prices = {symbol: current_price} if position > 0 else {}
            total_value = self.portfolio.get_total_value(current_prices)
            
            self.equity_curve.append({
                'date': current_date,
                'value': total_value,
                'price': current_price,
                'position': position
            })
        
        # Calculate final results
        final_price = float(df['Close'].iloc[-1])
        final_value = self.portfolio.get_total_value({symbol: final_price} if position > 0 else {})
        total_return = ((final_value - self.initial_cash) / self.initial_cash) * 100
        
        # Calculate metrics
        df_equity = pd.DataFrame(self.equity_curve)
        df_equity['returns'] = df_equity['value'].pct_change()
        
        sharpe_ratio = self._calculate_sharpe_ratio(df_equity['returns'].dropna())
        max_drawdown = self._calculate_max_drawdown(df_equity['value'])
        
        return {
            'strategy': f'SMA Crossover ({short_window}/{long_window})',
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'initial_value': self.initial_cash,
            'final_value': final_value,
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'equity_curve': self.equity_curve,
            'num_trades': num_trades
        }
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio
        
        Args:
            returns: Series of returns
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Sharpe ratio
        """
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
        
        # Annualize
        annual_return = returns.mean() * 252
        annual_std = returns.std() * np.sqrt(252)
        
        sharpe = (annual_return - risk_free_rate) / annual_std
        return float(sharpe)
    
    def _calculate_max_drawdown(self, equity_curve: pd.Series) -> float:
        """
        Calculate maximum drawdown
        
        Args:
            equity_curve: Series of portfolio values
            
        Returns:
            Maximum drawdown as percentage
        """
        if len(equity_curve) == 0:
            return 0.0
        
        # Calculate running maximum
        running_max = equity_curve.expanding().max()
        
        # Calculate drawdown
        drawdown = (equity_curve - running_max) / running_max * 100
        
        max_dd = drawdown.min()
        return float(max_dd)
    
    def reset(self):
        """Reset backtester to initial state"""
        self.portfolio = Portfolio(self.initial_cash)
        self.equity_curve = []
