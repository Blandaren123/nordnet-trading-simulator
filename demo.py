"""
Quick demo of the Nordnet Trading Simulator backend
Run this to see the simulator in action!
"""

from backend.portfolio import Portfolio
from backend.risk_calculator import RiskCalculator
from backend.what_if_simulator import WhatIfSimulator
from datetime import datetime, timedelta


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_portfolio():
    """Demo portfolio tracking"""
    print_section("📊 PORTFOLIO TRACKER DEMO")
    
    # Create portfolio
    portfolio = Portfolio(initial_cash=100000.0)
    print(f"Created portfolio with {portfolio.initial_cash:,.2f} SEK")
    
    # Make some trades
    print("\nExecuting trades...")
    portfolio.buy('AAPL', 50, 150.0)
    print("✓ Bought 50 AAPL @ 150.00")
    
    portfolio.buy('TSLA', 20, 250.0)
    print("✓ Bought 20 TSLA @ 250.00")
    
    portfolio.buy('MSFT', 30, 350.0)
    print("✓ Bought 30 MSFT @ 350.00")
    
    # Simulate current prices (slightly higher)
    current_prices = {
        'AAPL': 155.0,
        'TSLA': 245.0,  # Down
        'MSFT': 360.0
    }
    
    # Get summary
    summary = portfolio.get_summary(current_prices)
    
    print(f"\n📈 Portfolio Summary:")
    print(f"Total Value: {summary['total_value']:,.2f} SEK")
    print(f"Cash: {summary['cash']:,.2f} SEK")
    print(f"Invested: {summary['invested_value']:,.2f} SEK")
    print(f"Total Return: {summary['total_return']:.2f}%")
    print(f"Total Gain: {summary['total_gain']:,.2f} SEK")
    
    print(f"\n📋 Positions ({summary['num_positions']}):")
    for symbol, pos in summary['positions'].items():
        sign = "+" if pos['gain_pct'] >= 0 else ""
        color = "🟢" if pos['gain_pct'] >= 0 else "🔴"
        print(f"  {color} {symbol}: {pos['quantity']:.0f} shares @ {pos['current_price']:.2f} "
              f"= {pos['value']:,.2f} SEK ({sign}{pos['gain_pct']:.2f}%)")


def demo_risk_calculator():
    """Demo risk calculations"""
    print_section("⚖️ RISK/REWARD CALCULATOR DEMO")
    
    # Position sizing
    print("\nScenario: Account value 100,000 SEK, willing to risk 2%")
    print("Entry: 100 SEK, Stop Loss: 95 SEK")
    
    position = RiskCalculator.calculate_position_size(
        account_value=100000,
        risk_percentage=2.0,
        entry_price=100.0,
        stop_loss_price=95.0
    )
    
    print(f"\n📏 Position Size Calculation:")
    print(f"  Shares to buy: {position['position_size']:.0f}")
    print(f"  Total cost: {position['total_cost']:,.2f} SEK")
    print(f"  Max risk: {position['risk_amount']:,.2f} SEK")
    print(f"  Risk per share: {position['risk_per_share']:.2f} SEK")
    
    # Risk/Reward ratio
    print("\nScenario: Entry 100, Stop Loss 95, Take Profit 110")
    
    rr = RiskCalculator.calculate_risk_reward(
        entry_price=100.0,
        stop_loss_price=95.0,
        take_profit_price=110.0
    )
    
    print(f"\n🎯 Risk/Reward Analysis:")
    print(f"  Risk: {rr['risk']:.2f} SEK ({rr['risk_pct']:.2f}%)")
    print(f"  Reward: {rr['reward']:.2f} SEK ({rr['reward_pct']:.2f}%)")
    print(f"  Ratio: 1:{rr['risk_reward_ratio']:.2f}")
    
    if rr['risk_reward_ratio'] >= 2:
        print("  ✅ Good risk/reward ratio!")
    else:
        print("  ⚠️ Consider higher take profit or tighter stop loss")


def demo_what_if():
    """Demo what-if scenarios"""
    print_section("🚀 WHAT-IF SIMULATOR DEMO")
    
    print("\nNote: Using simulated data for demonstration")
    print("In production, this would fetch real historical data from Yahoo Finance")
    
    # Example scenario (mock data since we might not have internet access)
    print("\nScenario: What if I invested 100,000 SEK in a high-growth stock?")
    print("Entry: 50 SEK, Exit: 75 SEK (50% gain)")
    print("Holding period: 180 days")
    
    investment = 100000
    entry_price = 50.0
    exit_price = 75.0
    shares = investment / entry_price
    
    exit_value = shares * exit_price
    profit = exit_value - investment
    profit_pct = (profit / investment) * 100
    
    print(f"\n💰 Results:")
    print(f"  Initial investment: {investment:,.2f} SEK")
    print(f"  Shares purchased: {shares:,.2f}")
    print(f"  Final value: {exit_value:,.2f} SEK")
    print(f"  Profit: {profit:,.2f} SEK ({profit_pct:.2f}%)")
    print(f"  Annualized return: ~{(profit_pct * 365 / 180):.2f}%")


def demo_comparison():
    """Demo stock comparison"""
    print_section("📊 STOCK COMPARISON DEMO")
    
    print("\nComparing 3 hypothetical stocks with same 100,000 SEK investment:")
    
    scenarios = [
        {'symbol': 'STOCK-A', 'return_pct': 45.5, 'final': 145500},
        {'symbol': 'STOCK-B', 'return_pct': -12.3, 'final': 87700},
        {'symbol': 'STOCK-C', 'return_pct': 28.7, 'final': 128700},
    ]
    
    print("\n🏆 Results (sorted by performance):")
    for i, s in enumerate(sorted(scenarios, key=lambda x: x['return_pct'], reverse=True), 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        sign = "+" if s['return_pct'] >= 0 else ""
        print(f"  {medal} {s['symbol']}: {sign}{s['return_pct']:.1f}% → {s['final']:,.0f} SEK")
    
    best = max(scenarios, key=lambda x: x['return_pct'])
    worst = min(scenarios, key=lambda x: x['return_pct'])
    spread = best['return_pct'] - worst['return_pct']
    
    print(f"\n📈 Analysis:")
    print(f"  Best: {best['symbol']} ({best['return_pct']:.1f}%)")
    print(f"  Worst: {worst['symbol']} ({worst['return_pct']:.1f}%)")
    print(f"  Spread: {spread:.1f} percentage points")


def main():
    """Run all demos"""
    print("\n" + "🚀" * 30)
    print("  NORDNET TRADING SIMULATOR - QUICK DEMO")
    print("🚀" * 30)
    
    demo_portfolio()
    demo_risk_calculator()
    demo_what_if()
    demo_comparison()
    
    print_section("✨ DEMO COMPLETE!")
    print("\nTo start the full application:")
    print("  Backend: python -m backend.api")
    print("  Frontend: cd frontend && npm start")
    print("\nOr use the startup script:")
    print("  ./start.sh")
    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    main()
