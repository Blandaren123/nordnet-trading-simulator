"""
Stop Loss / Take Profit Simulator Module
Simulates trading with stop loss and take profit orders
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from .data_fetcher import DataFetcher


class StopLossTakeProfitSimulator:
    """Simulate trades with stop loss and take profit levels"""
    
    def __init__(self, initial_cash: float = 100000.0):
        """
        Initialize simulator
        
        Args:
            initial_cash: Starting cash amount
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.trades: List[Dict] = []
        
    def simulate_trade(
        self,
        symbol: str,
        entry_price: float,
        quantity: float,
        stop_loss_pct: float,
        take_profit_pct: float,
        start_date: str,
        end_date: Optional[str] = None,
        max_days: int = 365
    ) -> Dict:
        """
        Simulate a single trade with stop loss and take profit
        
        Args:
            symbol: Stock ticker symbol
            entry_price: Entry price per share
            quantity: Number of shares
            stop_loss_pct: Stop loss percentage (e.g., 5 for 5% below entry)
            take_profit_pct: Take profit percentage (e.g., 10 for 10% above entry)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date (optional, uses max_days if not provided)
            max_days: Maximum days to hold position
            
        Returns:
            Dict with simulation results
        """
        # Calculate stop loss and take profit prices
        stop_loss_price = entry_price * (1 - stop_loss_pct / 100)
        take_profit_price = entry_price * (1 + take_profit_pct / 100)
        
        # Fetch historical data
        if end_date:
            df = DataFetcher.get_historical_data(symbol, start_date, end_date)
        else:
            df = DataFetcher.get_historical_data(symbol, start_date, period="1y")
        
        if df.empty:
            return {'error': 'No data available for simulation'}
        
        # Limit to max_days
        df = df.head(max_days)
        
        # Simulate trade
        exit_price = None
        exit_date = None
        exit_reason = None
        
        for date, row in df.iterrows():
            low = float(row['Low'])
            high = float(row['High'])
            close = float(row['Close'])
            
            # Check if stop loss hit (use low of day)
            if low <= stop_loss_price:
                exit_price = stop_loss_price
                exit_date = date.to_pydatetime()
                exit_reason = 'Stop Loss'
                break
            
            # Check if take profit hit (use high of day)
            if high >= take_profit_price:
                exit_price = take_profit_price
                exit_date = date.to_pydatetime()
                exit_reason = 'Take Profit'
                break
        
        # If no exit, use last close price
        if exit_price is None:
            exit_price = float(df['Close'].iloc[-1])
            exit_date = df.index[-1].to_pydatetime()
            exit_reason = 'Max Days Reached' if len(df) >= max_days else 'End of Period'
        
        # Calculate results
        entry_cost = entry_price * quantity
        exit_value = exit_price * quantity
        profit_loss = exit_value - entry_cost
        profit_loss_pct = (profit_loss / entry_cost) * 100
        
        holding_days = (exit_date - pd.to_datetime(start_date)).days
        
        trade_result = {
            'symbol': symbol,
            'entry_date': start_date,
            'entry_price': entry_price,
            'exit_date': exit_date.strftime('%Y-%m-%d'),
            'exit_price': exit_price,
            'exit_reason': exit_reason,
            'quantity': quantity,
            'entry_cost': entry_cost,
            'exit_value': exit_value,
            'profit_loss': profit_loss,
            'profit_loss_pct': profit_loss_pct,
            'stop_loss_price': stop_loss_price,
            'take_profit_price': take_profit_price,
            'stop_loss_pct': stop_loss_pct,
            'take_profit_pct': take_profit_pct,
            'holding_days': holding_days,
            'success': exit_reason == 'Take Profit'
        }
        
        self.trades.append(trade_result)
        
        return trade_result
    
    def simulate_multiple_trades(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        stop_loss_pct: float,
        take_profit_pct: float,
        position_size_pct: float = 10.0,
        cooldown_days: int = 1
    ) -> Dict:
        """
        Simulate multiple trades over a period
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            stop_loss_pct: Stop loss percentage
            take_profit_pct: Take profit percentage
            position_size_pct: Percentage of cash to use per trade
            cooldown_days: Days to wait between trades
            
        Returns:
            Dict with aggregate results
        """
        df = DataFetcher.get_historical_data(symbol, start_date, end_date)
        
        if df.empty:
            return {'error': 'No data available for simulation'}
        
        trades = []
        current_cash = self.initial_cash
        i = 0
        
        while i < len(df):
            # Entry
            entry_date = df.index[i]
            entry_price = float(df['Close'].iloc[i])
            
            # Calculate position size
            position_value = current_cash * (position_size_pct / 100)
            quantity = position_value / entry_price
            
            if quantity == 0:
                break
            
            # Simulate this trade
            stop_loss_price = entry_price * (1 - stop_loss_pct / 100)
            take_profit_price = entry_price * (1 + take_profit_pct / 100)
            
            # Find exit
            exit_idx = None
            exit_price = None
            exit_reason = None
            
            for j in range(i, len(df)):
                row = df.iloc[j]
                low = float(row['Low'])
                high = float(row['High'])
                
                if low <= stop_loss_price:
                    exit_idx = j
                    exit_price = stop_loss_price
                    exit_reason = 'Stop Loss'
                    break
                
                if high >= take_profit_price:
                    exit_idx = j
                    exit_price = take_profit_price
                    exit_reason = 'Take Profit'
                    break
            
            # If no exit found, use last price
            if exit_idx is None:
                exit_idx = len(df) - 1
                exit_price = float(df['Close'].iloc[-1])
                exit_reason = 'End of Period'
            
            exit_date = df.index[exit_idx]
            
            # Calculate P&L
            entry_cost = entry_price * quantity
            exit_value = exit_price * quantity
            profit_loss = exit_value - entry_cost
            profit_loss_pct = (profit_loss / entry_cost) * 100
            
            current_cash = current_cash - entry_cost + exit_value
            
            trades.append({
                'entry_date': entry_date.strftime('%Y-%m-%d'),
                'entry_price': entry_price,
                'exit_date': exit_date.strftime('%Y-%m-%d'),
                'exit_price': exit_price,
                'exit_reason': exit_reason,
                'quantity': quantity,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'success': exit_reason == 'Take Profit'
            })
            
            # Move to next potential entry (after cooldown)
            i = exit_idx + cooldown_days
        
        # Calculate aggregate statistics
        if trades:
            total_trades = len(trades)
            winning_trades = sum(1 for t in trades if t['success'])
            losing_trades = total_trades - winning_trades
            win_rate = (winning_trades / total_trades) * 100
            
            total_profit = sum(t['profit_loss'] for t in trades if t['profit_loss'] > 0)
            total_loss = sum(abs(t['profit_loss']) for t in trades if t['profit_loss'] < 0)
            net_profit = sum(t['profit_loss'] for t in trades)
            net_profit_pct = ((current_cash - self.initial_cash) / self.initial_cash) * 100
            
            avg_win = total_profit / winning_trades if winning_trades > 0 else 0
            avg_loss = total_loss / losing_trades if losing_trades > 0 else 0
            
            profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
            
            return {
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date,
                'initial_cash': self.initial_cash,
                'final_cash': current_cash,
                'net_profit': net_profit,
                'net_profit_pct': net_profit_pct,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': win_rate,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'stop_loss_pct': stop_loss_pct,
                'take_profit_pct': take_profit_pct,
                'trades': trades
            }
        else:
            return {
                'error': 'No trades executed',
                'initial_cash': self.initial_cash
            }
    
    def optimize_sl_tp(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        sl_range: List[float] = [2, 5, 10, 15],
        tp_range: List[float] = [5, 10, 15, 20, 30]
    ) -> Dict:
        """
        Optimize stop loss and take profit percentages
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date
            end_date: End date
            sl_range: List of stop loss percentages to test
            tp_range: List of take profit percentages to test
            
        Returns:
            Dict with optimization results
        """
        results = []
        
        for sl in sl_range:
            for tp in tp_range:
                # Reset for each test
                self.cash = self.initial_cash
                self.trades = []
                
                result = self.simulate_multiple_trades(
                    symbol, start_date, end_date, sl, tp
                )
                
                if 'error' not in result:
                    results.append({
                        'stop_loss_pct': sl,
                        'take_profit_pct': tp,
                        'net_profit_pct': result['net_profit_pct'],
                        'win_rate': result['win_rate'],
                        'total_trades': result['total_trades'],
                        'profit_factor': result['profit_factor']
                    })
        
        if not results:
            return {'error': 'No valid results from optimization'}
        
        # Find best by net profit
        best_result = max(results, key=lambda x: x['net_profit_pct'])
        
        return {
            'symbol': symbol,
            'best_sl_pct': best_result['stop_loss_pct'],
            'best_tp_pct': best_result['take_profit_pct'],
            'best_net_profit_pct': best_result['net_profit_pct'],
            'best_win_rate': best_result['win_rate'],
            'all_results': results
        }
    
    def reset(self):
        """Reset simulator to initial state"""
        self.cash = self.initial_cash
        self.trades = []
