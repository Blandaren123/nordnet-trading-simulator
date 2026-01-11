"""
What-If Scenario Simulator
Simulates "all-in" scenarios on specific stocks
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .data_fetcher import DataFetcher


class WhatIfSimulator:
    """Simulate 'what-if' investment scenarios"""
    
    @staticmethod
    def all_in_scenario(
        symbol: str,
        investment_amount: float,
        start_date: str,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> Dict:
        """
        Simulate what would happen if you went all-in on a stock
        
        Args:
            symbol: Stock ticker symbol (e.g., 'RXRX', 'IONQ')
            investment_amount: Amount to invest
            start_date: Start date in YYYY-MM-DD format
            end_date: End date (optional)
            period: Period if end_date not provided
            
        Returns:
            Dict with scenario results
        """
        try:
            # Fetch historical data
            if end_date:
                df = DataFetcher.get_historical_data(symbol, start_date, end_date)
            else:
                df = DataFetcher.get_historical_data(symbol, start_date, period=period)
            
            if df.empty:
                return {'error': f'No data available for {symbol}'}
            
            # Entry
            entry_price = float(df['Close'].iloc[0])
            entry_date = df.index[0]
            shares = investment_amount / entry_price
            
            # Exit (current or end date)
            exit_price = float(df['Close'].iloc[-1])
            exit_date = df.index[-1]
            
            # Calculate returns
            exit_value = shares * exit_price
            profit_loss = exit_value - investment_amount
            profit_loss_pct = (profit_loss / investment_amount) * 100
            
            # Calculate additional metrics
            df['Daily_Return'] = df['Close'].pct_change()
            df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod()
            df['Portfolio_Value'] = investment_amount * df['Cumulative_Return']
            
            # Peak and drawdown
            peak_value = df['Portfolio_Value'].max()
            peak_date = df['Portfolio_Value'].idxmax()
            
            # Maximum drawdown
            running_max = df['Portfolio_Value'].expanding().max()
            drawdown = (df['Portfolio_Value'] - running_max) / running_max
            max_drawdown = drawdown.min() * 100
            max_drawdown_date = drawdown.idxmin()
            
            # Volatility
            annual_volatility = df['Daily_Return'].std() * np.sqrt(252) * 100
            
            # Best and worst days
            best_day_return = df['Daily_Return'].max() * 100
            best_day_date = df['Daily_Return'].idxmax()
            worst_day_return = df['Daily_Return'].min() * 100
            worst_day_date = df['Daily_Return'].idxmin()
            
            # Calculate holding period
            holding_days = (exit_date - entry_date).days
            
            # Annualized return
            years = holding_days / 365.25
            annualized_return = ((exit_value / investment_amount) ** (1 / years) - 1) * 100 if years > 0 else 0
            
            # Timeline data for charting
            timeline = []
            for date, row in df.iterrows():
                timeline.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'price': float(row['Close']),
                    'portfolio_value': float(row['Portfolio_Value']),
                    'return_pct': ((row['Portfolio_Value'] - investment_amount) / investment_amount) * 100
                })
            
            return {
                'symbol': symbol,
                'scenario': f'All-In on {symbol}',
                'entry_date': entry_date.strftime('%Y-%m-%d'),
                'entry_price': entry_price,
                'exit_date': exit_date.strftime('%Y-%m-%d'),
                'exit_price': exit_price,
                'shares': shares,
                'investment_amount': investment_amount,
                'exit_value': exit_value,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'holding_days': holding_days,
                'annualized_return': annualized_return,
                'peak_value': float(peak_value),
                'peak_date': peak_date.strftime('%Y-%m-%d'),
                'max_drawdown_pct': float(max_drawdown),
                'max_drawdown_date': max_drawdown_date.strftime('%Y-%m-%d'),
                'annual_volatility_pct': float(annual_volatility),
                'best_day_return_pct': float(best_day_return),
                'best_day_date': best_day_date.strftime('%Y-%m-%d'),
                'worst_day_return_pct': float(worst_day_return),
                'worst_day_date': worst_day_date.strftime('%Y-%m-%d'),
                'timeline': timeline
            }
        except Exception as e:
            return {'error': f'Error simulating scenario: {str(e)}'}
    
    @staticmethod
    def compare_scenarios(
        symbols: List[str],
        investment_amount: float,
        start_date: str,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> Dict:
        """
        Compare multiple all-in scenarios
        
        Args:
            symbols: List of stock ticker symbols
            investment_amount: Amount to invest in each
            start_date: Start date
            end_date: End date (optional)
            period: Period if end_date not provided
            
        Returns:
            Dict with comparison results
        """
        scenarios = []
        
        for symbol in symbols:
            result = WhatIfSimulator.all_in_scenario(
                symbol, investment_amount, start_date, end_date, period
            )
            
            if 'error' not in result:
                scenarios.append({
                    'symbol': symbol,
                    'profit_loss': result['profit_loss'],
                    'profit_loss_pct': result['profit_loss_pct'],
                    'exit_value': result['exit_value'],
                    'max_drawdown_pct': result['max_drawdown_pct'],
                    'annual_volatility_pct': result['annual_volatility_pct'],
                    'annualized_return': result['annualized_return']
                })
        
        if not scenarios:
            return {'error': 'No valid scenarios generated'}
        
        # Find best and worst
        best = max(scenarios, key=lambda x: x['profit_loss_pct'])
        worst = min(scenarios, key=lambda x: x['profit_loss_pct'])
        
        return {
            'investment_amount': investment_amount,
            'start_date': start_date,
            'end_date': end_date or f'{period} from start',
            'scenarios': scenarios,
            'best_performer': {
                'symbol': best['symbol'],
                'return_pct': best['profit_loss_pct'],
                'final_value': best['exit_value']
            },
            'worst_performer': {
                'symbol': worst['symbol'],
                'return_pct': worst['profit_loss_pct'],
                'final_value': worst['exit_value']
            },
            'spread': best['profit_loss_pct'] - worst['profit_loss_pct']
        }
    
    @staticmethod
    def dollar_cost_average_scenario(
        symbol: str,
        monthly_investment: float,
        start_date: str,
        end_date: str
    ) -> Dict:
        """
        Simulate dollar-cost averaging strategy
        
        Args:
            symbol: Stock ticker symbol
            monthly_investment: Amount to invest monthly
            start_date: Start date
            end_date: End date
            
        Returns:
            Dict with DCA results
        """
        try:
            df = DataFetcher.get_historical_data(symbol, start_date, end_date)
            
            if df.empty:
                return {'error': f'No data available for {symbol}'}
            
            # Resample to monthly
            df_monthly = df.resample('MS').first()  # First day of month
            
            total_invested = 0
            total_shares = 0
            purchases = []
            
            for date, row in df_monthly.iterrows():
                price = float(row['Close'])
                shares = monthly_investment / price
                total_shares += shares
                total_invested += monthly_investment
                
                purchases.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'price': price,
                    'shares': shares,
                    'amount': monthly_investment,
                    'total_shares': total_shares,
                    'total_invested': total_invested
                })
            
            # Final value
            final_price = float(df['Close'].iloc[-1])
            final_value = total_shares * final_price
            profit_loss = final_value - total_invested
            profit_loss_pct = (profit_loss / total_invested) * 100
            
            avg_price = total_invested / total_shares if total_shares > 0 else 0
            
            return {
                'symbol': symbol,
                'strategy': 'Dollar-Cost Averaging',
                'start_date': start_date,
                'end_date': end_date,
                'monthly_investment': monthly_investment,
                'total_invested': total_invested,
                'total_shares': total_shares,
                'avg_price': avg_price,
                'final_price': final_price,
                'final_value': final_value,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'num_purchases': len(purchases),
                'purchases': purchases
            }
        except Exception as e:
            return {'error': f'Error simulating DCA: {str(e)}'}
    
    @staticmethod
    def lump_sum_vs_dca(
        symbol: str,
        total_amount: float,
        start_date: str,
        end_date: str,
        dca_periods: int = 12
    ) -> Dict:
        """
        Compare lump sum vs dollar-cost averaging
        
        Args:
            symbol: Stock ticker symbol
            total_amount: Total amount to invest
            start_date: Start date
            end_date: End date
            dca_periods: Number of periods for DCA (default 12 months)
            
        Returns:
            Dict comparing both strategies
        """
        # Lump sum
        lump_sum = WhatIfSimulator.all_in_scenario(
            symbol, total_amount, start_date, end_date
        )
        
        # DCA
        monthly_amount = total_amount / dca_periods
        dca = WhatIfSimulator.dollar_cost_average_scenario(
            symbol, monthly_amount, start_date, end_date
        )
        
        if 'error' in lump_sum or 'error' in dca:
            return {'error': 'Could not complete comparison'}
        
        return {
            'symbol': symbol,
            'total_amount': total_amount,
            'start_date': start_date,
            'end_date': end_date,
            'lump_sum': {
                'final_value': lump_sum['exit_value'],
                'return_pct': lump_sum['profit_loss_pct'],
                'max_drawdown_pct': lump_sum['max_drawdown_pct']
            },
            'dca': {
                'final_value': dca['final_value'],
                'return_pct': dca['profit_loss_pct'],
                'num_purchases': dca['num_purchases']
            },
            'winner': 'Lump Sum' if lump_sum['exit_value'] > dca['final_value'] else 'DCA',
            'difference': abs(lump_sum['exit_value'] - dca['final_value']),
            'difference_pct': ((lump_sum['exit_value'] - dca['final_value']) / total_amount) * 100
        }
