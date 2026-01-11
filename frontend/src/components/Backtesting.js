import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Backtesting() {
  const [symbol, setSymbol] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [strategy, setStrategy] = useState('buy-hold');
  const [initialCash, setInitialCash] = useState('100000');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runBacktest = async () => {
    setLoading(true);
    setError('');
    setResults(null);

    try {
      let response;
      if (strategy === 'buy-hold') {
        response = await axios.post(`${API_URL}/backtest/buy-hold`, {
          symbol,
          start_date: startDate,
          end_date: endDate,
          initial_cash: parseFloat(initialCash)
        });
      } else {
        response = await axios.post(`${API_URL}/backtest/sma-crossover`, {
          symbol,
          start_date: startDate,
          end_date: endDate,
          initial_cash: parseFloat(initialCash),
          short_window: 50,
          long_window: 200
        });
      }

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResults(response.data);
      }
    } catch (err) {
      setError('Failed to run backtest: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h2>Backtesting Simulator</h2>
        <p>Test trading strategies on historical data</p>

        {error && <div className="error">{error}</div>}

        <div className="form-row">
          <div className="form-group">
            <label>Symbol</label>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="AAPL"
            />
          </div>
          <div className="form-group">
            <label>Strategy</label>
            <select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
              <option value="buy-hold">Buy and Hold</option>
              <option value="sma-crossover">SMA Crossover (50/200)</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Initial Cash</label>
            <input
              type="number"
              value={initialCash}
              onChange={(e) => setInitialCash(e.target.value)}
              placeholder="100000"
            />
          </div>
        </div>

        <button 
          className="btn btn-primary" 
          onClick={runBacktest}
          disabled={loading || !symbol || !startDate || !endDate}
        >
          {loading ? 'Running Backtest...' : 'Run Backtest'}
        </button>
      </div>

      {results && (
        <div className="card">
          <h3>Backtest Results</h3>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Strategy</div>
              <div className="stat-value" style={{ fontSize: '1rem' }}>{results.strategy}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Initial Value</div>
              <div className="stat-value">{results.initial_value.toFixed(2)}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Final Value</div>
              <div className="stat-value">{results.final_value.toFixed(2)}</div>
            </div>
            <div className={`stat-card ${results.total_return >= 0 ? 'positive' : 'negative'}`}>
              <div className="stat-label">Total Return</div>
              <div className="stat-value">{results.total_return.toFixed(2)}%</div>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Sharpe Ratio</div>
              <div className="stat-value">{results.sharpe_ratio.toFixed(2)}</div>
            </div>
            <div className="stat-card negative">
              <div className="stat-label">Max Drawdown</div>
              <div className="stat-value">{results.max_drawdown.toFixed(2)}%</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Number of Trades</div>
              <div className="stat-value">{results.num_trades}</div>
            </div>
          </div>

          {results.equity_curve && results.equity_curve.length > 0 && (
            <div style={{ marginTop: '2rem' }}>
              <h3>Equity Curve</h3>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={results.equity_curve}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={(date) => new Date(date).toLocaleDateString()}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(date) => new Date(date).toLocaleDateString()}
                    formatter={(value) => value.toFixed(2)}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    stroke="#667eea" 
                    strokeWidth={2}
                    name="Portfolio Value"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Backtesting;
