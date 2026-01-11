"""
Flask API for Nordnet Trading Simulator
Provides REST endpoints for portfolio tracking, backtesting, and risk analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

from .portfolio import Portfolio
from .backtesting import Backtester
from .risk_calculator import RiskCalculator
from .stop_loss_simulator import StopLossTakeProfitSimulator
from .what_if_simulator import WhatIfSimulator
from .data_fetcher import DataFetcher

app = Flask(__name__)
CORS(app)

# Global instances (in production, use sessions or database)
portfolios = {}
backtesters = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


# Portfolio endpoints
@app.route('/api/portfolio/create', methods=['POST'])
def create_portfolio():
    """Create a new portfolio"""
    data = request.json
    portfolio_id = data.get('portfolio_id', 'default')
    initial_cash = data.get('initial_cash', 100000.0)
    
    portfolios[portfolio_id] = Portfolio(initial_cash)
    
    return jsonify({
        'success': True,
        'portfolio_id': portfolio_id,
        'initial_cash': initial_cash
    })


@app.route('/api/portfolio/<portfolio_id>/buy', methods=['POST'])
def portfolio_buy(portfolio_id):
    """Execute buy order"""
    if portfolio_id not in portfolios:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    data = request.json
    symbol = data.get('symbol')
    quantity = data.get('quantity')
    price = data.get('price')
    
    if not all([symbol, quantity, price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    portfolio = portfolios[portfolio_id]
    success = portfolio.buy(symbol, float(quantity), float(price))
    
    return jsonify({
        'success': success,
        'message': 'Buy order executed' if success else 'Insufficient funds'
    })


@app.route('/api/portfolio/<portfolio_id>/sell', methods=['POST'])
def portfolio_sell(portfolio_id):
    """Execute sell order"""
    if portfolio_id not in portfolios:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    data = request.json
    symbol = data.get('symbol')
    quantity = data.get('quantity')
    price = data.get('price')
    
    if not all([symbol, quantity, price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    portfolio = portfolios[portfolio_id]
    success = portfolio.sell(symbol, float(quantity), float(price))
    
    return jsonify({
        'success': success,
        'message': 'Sell order executed' if success else 'Insufficient holdings'
    })


@app.route('/api/portfolio/<portfolio_id>/summary', methods=['GET'])
def portfolio_summary(portfolio_id):
    """Get portfolio summary"""
    if portfolio_id not in portfolios:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    portfolio = portfolios[portfolio_id]
    
    # Get current prices for holdings
    symbols = list(portfolio.holdings.keys())
    current_prices = DataFetcher.get_multiple_current_prices(symbols) if symbols else {}
    
    summary = portfolio.get_summary(current_prices)
    
    return jsonify(summary)


@app.route('/api/portfolio/<portfolio_id>/transactions', methods=['GET'])
def portfolio_transactions(portfolio_id):
    """Get transaction history"""
    if portfolio_id not in portfolios:
        return jsonify({'error': 'Portfolio not found'}), 404
    
    portfolio = portfolios[portfolio_id]
    transactions = portfolio.transactions
    
    # Convert datetime objects to strings
    for t in transactions:
        if isinstance(t['date'], datetime):
            t['date'] = t['date'].isoformat()
    
    return jsonify({'transactions': transactions})


# Data endpoints
@app.route('/api/data/historical', methods=['GET'])
def get_historical_data():
    """Get historical price data"""
    symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    period = request.args.get('period', '1y')
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    try:
        df = DataFetcher.get_historical_data(symbol, start_date, end_date, period)
        
        # Convert to JSON-friendly format
        data = []
        for date, row in df.iterrows():
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
        
        return jsonify({'symbol': symbol, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/price', methods=['GET'])
def get_current_price():
    """Get current price"""
    symbol = request.args.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    try:
        price = DataFetcher.get_current_price(symbol)
        return jsonify({'symbol': symbol, 'price': price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/info', methods=['GET'])
def get_stock_info():
    """Get stock information"""
    symbol = request.args.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    info = DataFetcher.get_stock_info(symbol)
    return jsonify(info)


# Backtesting endpoints
@app.route('/api/backtest/buy-hold', methods=['POST'])
def backtest_buy_hold():
    """Run buy and hold backtest"""
    data = request.json
    symbol = data.get('symbol')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    initial_cash = data.get('initial_cash', 100000.0)
    allocation = data.get('allocation', 1.0)
    
    if not all([symbol, start_date, end_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        backtester = Backtester(initial_cash)
        results = backtester.run_buy_and_hold(symbol, start_date, end_date, allocation)
        
        # Convert datetime objects to strings
        for point in results.get('equity_curve', []):
            if isinstance(point['date'], datetime):
                point['date'] = point['date'].isoformat()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/backtest/sma-crossover', methods=['POST'])
def backtest_sma_crossover():
    """Run SMA crossover backtest"""
    data = request.json
    symbol = data.get('symbol')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    initial_cash = data.get('initial_cash', 100000.0)
    short_window = data.get('short_window', 50)
    long_window = data.get('long_window', 200)
    allocation = data.get('allocation', 1.0)
    
    if not all([symbol, start_date, end_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        backtester = Backtester(initial_cash)
        results = backtester.run_sma_crossover(
            symbol, start_date, end_date, short_window, long_window, allocation
        )
        
        # Convert datetime objects to strings
        for point in results.get('equity_curve', []):
            if isinstance(point['date'], datetime):
                point['date'] = point['date'].isoformat()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Risk calculation endpoints
@app.route('/api/risk/position-size', methods=['POST'])
def calculate_position_size():
    """Calculate position size"""
    data = request.json
    account_value = data.get('account_value')
    risk_percentage = data.get('risk_percentage')
    entry_price = data.get('entry_price')
    stop_loss_price = data.get('stop_loss_price')
    
    if not all([account_value, risk_percentage, entry_price, stop_loss_price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = RiskCalculator.calculate_position_size(
        float(account_value),
        float(risk_percentage),
        float(entry_price),
        float(stop_loss_price)
    )
    
    return jsonify(result)


@app.route('/api/risk/risk-reward', methods=['POST'])
def calculate_risk_reward():
    """Calculate risk/reward ratio"""
    data = request.json
    entry_price = data.get('entry_price')
    stop_loss_price = data.get('stop_loss_price')
    take_profit_price = data.get('take_profit_price')
    
    if not all([entry_price, stop_loss_price, take_profit_price]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = RiskCalculator.calculate_risk_reward(
        float(entry_price),
        float(stop_loss_price),
        float(take_profit_price)
    )
    
    return jsonify(result)


# Stop loss / Take profit simulator endpoints
@app.route('/api/sltp/simulate', methods=['POST'])
def simulate_sltp():
    """Simulate trade with stop loss and take profit"""
    data = request.json
    symbol = data.get('symbol')
    entry_price = data.get('entry_price')
    quantity = data.get('quantity')
    stop_loss_pct = data.get('stop_loss_pct')
    take_profit_pct = data.get('take_profit_pct')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    initial_cash = data.get('initial_cash', 100000.0)
    
    if not all([symbol, entry_price, quantity, stop_loss_pct, take_profit_pct, start_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        simulator = StopLossTakeProfitSimulator(initial_cash)
        result = simulator.simulate_trade(
            symbol,
            float(entry_price),
            float(quantity),
            float(stop_loss_pct),
            float(take_profit_pct),
            start_date,
            end_date
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sltp/optimize', methods=['POST'])
def optimize_sltp():
    """Optimize stop loss and take profit levels"""
    data = request.json
    symbol = data.get('symbol')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    initial_cash = data.get('initial_cash', 100000.0)
    
    if not all([symbol, start_date, end_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        simulator = StopLossTakeProfitSimulator(initial_cash)
        result = simulator.optimize_sl_tp(symbol, start_date, end_date)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# What-if simulator endpoints
@app.route('/api/whatif/all-in', methods=['POST'])
def what_if_all_in():
    """Simulate all-in scenario"""
    data = request.json
    symbol = data.get('symbol')
    investment_amount = data.get('investment_amount')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    period = data.get('period', '1y')
    
    if not all([symbol, investment_amount, start_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = WhatIfSimulator.all_in_scenario(
            symbol,
            float(investment_amount),
            start_date,
            end_date,
            period
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/whatif/compare', methods=['POST'])
def what_if_compare():
    """Compare multiple all-in scenarios"""
    data = request.json
    symbols = data.get('symbols')
    investment_amount = data.get('investment_amount')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    period = data.get('period', '1y')
    
    if not all([symbols, investment_amount, start_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = WhatIfSimulator.compare_scenarios(
            symbols,
            float(investment_amount),
            start_date,
            end_date,
            period
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/whatif/dca', methods=['POST'])
def what_if_dca():
    """Simulate dollar-cost averaging"""
    data = request.json
    symbol = data.get('symbol')
    monthly_investment = data.get('monthly_investment')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if not all([symbol, monthly_investment, start_date, end_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = WhatIfSimulator.dollar_cost_average_scenario(
            symbol,
            float(monthly_investment),
            start_date,
            end_date
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/whatif/lump-vs-dca', methods=['POST'])
def what_if_lump_vs_dca():
    """Compare lump sum vs DCA"""
    data = request.json
    symbol = data.get('symbol')
    total_amount = data.get('total_amount')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    dca_periods = data.get('dca_periods', 12)
    
    if not all([symbol, total_amount, start_date, end_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = WhatIfSimulator.lump_sum_vs_dca(
            symbol,
            float(total_amount),
            start_date,
            end_date,
            int(dca_periods)
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
