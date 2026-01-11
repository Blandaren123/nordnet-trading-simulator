"""
Risk/Reward Calculator Module
Calculate risk metrics, position sizing, and risk/reward ratios
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional


class RiskCalculator:
    """Calculate risk metrics and position sizing"""
    
    @staticmethod
    def calculate_position_size(
        account_value: float,
        risk_percentage: float,
        entry_price: float,
        stop_loss_price: float
    ) -> Dict:
        """
        Calculate position size based on risk parameters
        
        Args:
            account_value: Total account value
            risk_percentage: Percentage of account to risk (e.g., 2 for 2%)
            entry_price: Intended entry price
            stop_loss_price: Stop loss price
            
        Returns:
            Dict with position size and risk metrics
        """
        risk_amount = account_value * (risk_percentage / 100)
        risk_per_share = abs(entry_price - stop_loss_price)
        
        if risk_per_share == 0:
            return {
                'error': 'Entry price and stop loss cannot be the same',
                'position_size': 0,
                'risk_amount': 0
            }
        
        position_size = risk_amount / risk_per_share
        total_cost = position_size * entry_price
        
        return {
            'position_size': position_size,
            'total_cost': total_cost,
            'risk_amount': risk_amount,
            'risk_per_share': risk_per_share,
            'account_risk_pct': risk_percentage
        }
    
    @staticmethod
    def calculate_risk_reward(
        entry_price: float,
        stop_loss_price: float,
        take_profit_price: float
    ) -> Dict:
        """
        Calculate risk/reward ratio
        
        Args:
            entry_price: Entry price
            stop_loss_price: Stop loss price
            take_profit_price: Take profit price
            
        Returns:
            Dict with risk/reward metrics
        """
        risk = abs(entry_price - stop_loss_price)
        reward = abs(take_profit_price - entry_price)
        
        if risk == 0:
            return {
                'error': 'Risk cannot be zero',
                'risk_reward_ratio': 0
            }
        
        risk_reward_ratio = reward / risk
        risk_pct = (risk / entry_price) * 100
        reward_pct = (reward / entry_price) * 100
        
        return {
            'risk': risk,
            'reward': reward,
            'risk_reward_ratio': risk_reward_ratio,
            'risk_pct': risk_pct,
            'reward_pct': reward_pct,
            'entry_price': entry_price,
            'stop_loss_price': stop_loss_price,
            'take_profit_price': take_profit_price
        }
    
    @staticmethod
    def calculate_portfolio_var(
        returns: pd.Series,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Calculate Value at Risk (VaR) for portfolio
        
        Args:
            returns: Series of portfolio returns
            confidence_level: Confidence level (e.g., 0.95 for 95%)
            
        Returns:
            Dict with VaR metrics
        """
        if len(returns) == 0:
            return {
                'var': 0,
                'cvar': 0,
                'confidence_level': confidence_level
            }
        
        # Calculate VaR
        var = np.percentile(returns, (1 - confidence_level) * 100)
        
        # Calculate Conditional VaR (CVaR) - expected loss beyond VaR
        cvar = returns[returns <= var].mean()
        
        return {
            'var': float(var),
            'cvar': float(cvar) if not np.isnan(cvar) else 0.0,
            'confidence_level': confidence_level,
            'interpretation': f'{confidence_level*100}% confident losses will not exceed {abs(var)*100:.2f}%'
        }
    
    @staticmethod
    def calculate_volatility(returns: pd.Series, annualize: bool = True) -> Dict:
        """
        Calculate volatility metrics
        
        Args:
            returns: Series of returns
            annualize: Whether to annualize the volatility
            
        Returns:
            Dict with volatility metrics
        """
        if len(returns) == 0:
            return {
                'volatility': 0,
                'annualized': annualize
            }
        
        volatility = returns.std()
        
        if annualize:
            volatility = volatility * np.sqrt(252)  # Assuming daily returns
        
        return {
            'volatility': float(volatility),
            'volatility_pct': float(volatility * 100),
            'annualized': annualize,
            'mean_return': float(returns.mean()),
            'max_return': float(returns.max()),
            'min_return': float(returns.min())
        }
    
    @staticmethod
    def calculate_kelly_criterion(
        win_rate: float,
        avg_win: float,
        avg_loss: float
    ) -> Dict:
        """
        Calculate Kelly Criterion for optimal position sizing
        
        Args:
            win_rate: Probability of winning (0 to 1)
            avg_win: Average winning return
            avg_loss: Average losing return (positive number)
            
        Returns:
            Dict with Kelly percentage
        """
        if avg_loss == 0:
            return {
                'error': 'Average loss cannot be zero',
                'kelly_pct': 0
            }
        
        # Kelly formula: W - [(1-W) / R]
        # where W = win rate, R = avg_win/avg_loss
        win_loss_ratio = avg_win / avg_loss
        kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
        
        # Apply half-Kelly for safety
        half_kelly = kelly * 0.5
        
        return {
            'kelly_pct': float(kelly * 100),
            'half_kelly_pct': float(half_kelly * 100),
            'win_rate': win_rate,
            'win_loss_ratio': win_loss_ratio,
            'recommendation': 'Use half-Kelly for more conservative sizing'
        }
    
    @staticmethod
    def calculate_beta(
        stock_returns: pd.Series,
        market_returns: pd.Series
    ) -> Dict:
        """
        Calculate beta relative to market
        
        Args:
            stock_returns: Series of stock returns
            market_returns: Series of market returns
            
        Returns:
            Dict with beta and related metrics
        """
        if len(stock_returns) == 0 or len(market_returns) == 0:
            return {
                'beta': 1.0,
                'alpha': 0.0,
                'r_squared': 0.0
            }
        
        # Align the series
        aligned = pd.concat([stock_returns, market_returns], axis=1, join='inner')
        aligned.columns = ['stock', 'market']
        
        # Calculate covariance and variance
        covariance = aligned['stock'].cov(aligned['market'])
        market_variance = aligned['market'].var()
        
        if market_variance == 0:
            return {
                'beta': 1.0,
                'alpha': 0.0,
                'r_squared': 0.0
            }
        
        beta = covariance / market_variance
        
        # Calculate alpha (Jensen's alpha)
        alpha = aligned['stock'].mean() - (beta * aligned['market'].mean())
        
        # Calculate R-squared
        correlation = aligned['stock'].corr(aligned['market'])
        r_squared = correlation ** 2
        
        return {
            'beta': float(beta),
            'alpha': float(alpha),
            'r_squared': float(r_squared),
            'interpretation': f"Stock is {'more' if beta > 1 else 'less'} volatile than market"
        }
