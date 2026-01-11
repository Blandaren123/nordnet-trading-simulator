"""
Data Fetcher Module
Fetches historical stock price data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


class DataFetcher:
    """Fetch historical stock price data"""
    
    @staticmethod
    def get_historical_data(
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        Fetch historical price data for a stock
        
        Args:
            symbol: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            period: Period to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame with historical price data
        """
        try:
            ticker = yf.Ticker(symbol)
            
            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)
            
            if df.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            return df
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    @staticmethod
    def get_current_price(symbol: str) -> float:
        """
        Get current price for a stock
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Current price
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            return float(data['Close'].iloc[-1])
        except Exception as e:
            raise Exception(f"Error fetching current price for {symbol}: {str(e)}")
    
    @staticmethod
    def get_multiple_current_prices(symbols: list) -> dict:
        """
        Get current prices for multiple stocks
        
        Args:
            symbols: List of stock ticker symbols
            
        Returns:
            Dict of symbol -> current price
        """
        prices = {}
        for symbol in symbols:
            try:
                prices[symbol] = DataFetcher.get_current_price(symbol)
            except Exception as e:
                print(f"Warning: Could not fetch price for {symbol}: {e}")
                prices[symbol] = 0.0
        return prices
    
    @staticmethod
    def get_stock_info(symbol: str) -> dict:
        """
        Get stock information
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dict with stock info
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            return {
                'symbol': symbol,
                'name': symbol,
                'sector': 'N/A',
                'industry': 'N/A',
                'market_cap': 0,
                'currency': 'USD'
            }
