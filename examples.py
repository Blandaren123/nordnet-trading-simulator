"""
Example usage scripts for the Nordnet Trading Simulator
Demonstrates how to use the backend API directly
"""

from backend.portfolio import Portfolio
from backend.backtesting import Backtester
from backend.risk_calculator import RiskCalculator
from backend.stop_loss_simulator import StopLossTakeProfitSimulator
from backend.what_if_simulator import WhatIfSimulator
from backend.data_fetcher import DataFetcher


def example_portfolio():
    """Example: Portfolio tracking"""
    print("\n=== Portfolio Tracker Example ===")
    
    # Create portfolio with 100,000 SEK
    portfolio = Portfolio(initial_cash=100000.0)
    
    # Buy some stocks
    portfolio.buy('AAPL', 10, 150.0)
    portfolio.buy('TSLA', 5, 250.0)
    
    # Get current prices
    current_prices = DataFetcher.get_multiple_current_prices(['AAPL', 'TSLA'])
    
    # Get portfolio summary
    summary = portfolio.get_summary(current_prices)
    
    print(f"Total Value: {summary['total_value']:.2f} SEK")
    print(f"Total Return: {summary['total_return']:.2f}%")
    print(f"Cash: {summary['cash']:.2f} SEK")
    print("\nPositions:")
    for symbol, position in summary['positions'].items():
        print(f"  {symbol}: {position['quantity']:.2f} shares @ {position['current_price']:.2f} = {position['value']:.2f} SEK ({position['gain_pct']:.2f}%)")


def example_backtesting():
    """Example: Backtesting strategies"""
    print("\n=== Backtesting Example ===")
    
    # Create backtester
    backtester = Backtester(initial_cash=100000.0)
    
    # Run buy-and-hold strategy
    results = backtester.run_buy_and_hold(
        symbol='AAPL',
        start_date='2023-01-01',
        end_date='2024-01-01',
        allocation=1.0
    )
    
    print(f"Strategy: {results['strategy']}")
    print(f"Symbol: {results['symbol']}")
    print(f"Initial Value: {results['initial_value']:.2f} SEK")
    print(f"Final Value: {results['final_value']:.2f} SEK")
    print(f"Total Return: {results['total_return']:.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2f}%")


def example_risk_calculator():
    """Example: Risk/Reward calculations"""
    print("\n=== Risk Calculator Example ===")
    
    # Calculate position size
    position_size = RiskCalculator.calculate_position_size(
        account_value=100000.0,
        risk_percentage=2.0,
        entry_price=100.0,
        stop_loss_price=95.0
    )
    
    print("Position Size Calculation:")
    print(f"  Shares to buy: {position_size['position_size']:.2f}")
    print(f"  Total cost: {position_size['total_cost']:.2f} SEK")
    print(f"  Risk amount: {position_size['risk_amount']:.2f} SEK")
    
    # Calculate risk/reward ratio
    risk_reward = RiskCalculator.calculate_risk_reward(
        entry_price=100.0,
        stop_loss_price=95.0,
        take_profit_price=110.0
    )
    
    print("\nRisk/Reward Calculation:")
    print(f"  Risk: {risk_reward['risk']:.2f} ({risk_reward['risk_pct']:.2f}%)")
    print(f"  Reward: {risk_reward['reward']:.2f} ({risk_reward['reward_pct']:.2f}%)")
    print(f"  R/R Ratio: 1:{risk_reward['risk_reward_ratio']:.2f}")


def example_stop_loss_simulator():
    """Example: Stop loss / take profit simulation"""
    print("\n=== Stop Loss/Take Profit Simulator Example ===")
    
    simulator = StopLossTakeProfitSimulator(initial_cash=100000.0)
    
    # Simulate a trade
    result = simulator.simulate_trade(
        symbol='AAPL',
        entry_price=150.0,
        quantity=100,
        stop_loss_pct=5.0,
        take_profit_pct=10.0,
        start_date='2024-01-01',
        max_days=90
    )
    
    print(f"Symbol: {result['symbol']}")
    print(f"Entry: {result['entry_price']:.2f} on {result['entry_date']}")
    print(f"Exit: {result['exit_price']:.2f} on {result['exit_date']}")
    print(f"Exit Reason: {result['exit_reason']}")
    print(f"P&L: {result['profit_loss']:.2f} SEK ({result['profit_loss_pct']:.2f}%)")
    print(f"Holding Period: {result['holding_days']} days")


def example_what_if_simulator():
    """Example: What-if scenario simulation"""
    print("\n=== What-If Simulator Example ===")
    
    # Simulate all-in on a stock
    result = WhatIfSimulator.all_in_scenario(
        symbol='IONQ',
        investment_amount=100000.0,
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    
    if 'error' not in result:
        print(f"All-In Scenario: {result['symbol']}")
        print(f"Investment: {result['investment_amount']:.2f} SEK")
        print(f"Final Value: {result['exit_value']:.2f} SEK")
        print(f"Profit/Loss: {result['profit_loss']:.2f} SEK ({result['profit_loss_pct']:.2f}%)")
        print(f"Peak Value: {result['peak_value']:.2f} SEK on {result['peak_date']}")
        print(f"Max Drawdown: {result['max_drawdown_pct']:.2f}%")
        print(f"Annualized Return: {result['annualized_return']:.2f}%")
    else:
        print(f"Error: {result['error']}")


def example_comparison():
    """Example: Compare multiple stocks"""
    print("\n=== Stock Comparison Example ===")
    
    result = WhatIfSimulator.compare_scenarios(
        symbols=['RXRX', 'IONQ', 'AAPL'],
        investment_amount=100000.0,
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    
    if 'error' not in result:
        print("Comparison Results:")
        print(f"Best Performer: {result['best_performer']['symbol']} with {result['best_performer']['return_pct']:.2f}% return")
        print(f"Worst Performer: {result['worst_performer']['symbol']} with {result['worst_performer']['return_pct']:.2f}% return")
        print(f"Spread: {result['spread']:.2f}%")
        
        print("\nDetailed Results:")
        for scenario in result['scenarios']:
            print(f"  {scenario['symbol']}: {scenario['profit_loss_pct']:.2f}% return")


if __name__ == '__main__':
    print("🚀 Nordnet Trading Simulator - Example Usage")
    print("=" * 50)
    
    # Run all examples
    try:
        example_portfolio()
    except Exception as e:
        print(f"Portfolio example error: {e}")
    
    try:
        example_backtesting()
    except Exception as e:
        print(f"Backtesting example error: {e}")
    
    try:
        example_risk_calculator()
    except Exception as e:
        print(f"Risk calculator example error: {e}")
    
    try:
        example_stop_loss_simulator()
    except Exception as e:
        print(f"Stop loss simulator example error: {e}")
    
    try:
        example_what_if_simulator()
    except Exception as e:
        print(f"What-if simulator example error: {e}")
    
    try:
        example_comparison()
    except Exception as e:
        print(f"Comparison example error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Examples completed!")
