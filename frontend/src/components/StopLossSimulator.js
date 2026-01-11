import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function StopLossSimulator() {
  const [symbol, setSymbol] = useState('');
  const [entryPrice, setEntryPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [stopLossPct, setStopLossPct] = useState('5');
  const [takeProfitPct, setTakeProfitPct] = useState('10');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [result, setResult] = useState(null);
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const simulateTrade = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/sltp/simulate`, {
        symbol,
        entry_price: parseFloat(entryPrice),
        quantity: parseFloat(quantity),
        stop_loss_pct: parseFloat(stopLossPct),
        take_profit_pct: parseFloat(takeProfitPct),
        start_date: startDate,
        end_date: endDate
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError('Failed to simulate trade: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const optimizeSLTP = async () => {
    setLoading(true);
    setError('');
    setOptimizationResult(null);

    try {
      const response = await axios.post(`${API_URL}/sltp/optimize`, {
        symbol,
        start_date: startDate,
        end_date: endDate
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setOptimizationResult(response.data);
      }
    } catch (err) {
      setError('Failed to optimize: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h2>Stop Loss / Take Profit Simulator</h2>
        <p>Simulate trades with stop loss and take profit levels</p>

        {error && <div className="error">{error}</div>}

        <h3>Trade Parameters</h3>
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
            <label>Entry Price</label>
            <input
              type="number"
              value={entryPrice}
              onChange={(e) => setEntryPrice(e.target.value)}
              placeholder="100.00"
              step="0.01"
            />
          </div>
          <div className="form-group">
            <label>Quantity</label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder="100"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Stop Loss (%)</label>
            <input
              type="number"
              value={stopLossPct}
              onChange={(e) => setStopLossPct(e.target.value)}
              placeholder="5"
              step="0.1"
            />
          </div>
          <div className="form-group">
            <label>Take Profit (%)</label>
            <input
              type="number"
              value={takeProfitPct}
              onChange={(e) => setTakeProfitPct(e.target.value)}
              placeholder="10"
              step="0.1"
            />
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
            <label>End Date (optional)</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button 
            className="btn btn-primary" 
            onClick={simulateTrade}
            disabled={loading || !symbol || !entryPrice || !quantity || !startDate}
          >
            {loading ? 'Simulating...' : 'Simulate Trade'}
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={optimizeSLTP}
            disabled={loading || !symbol || !startDate || !endDate}
          >
            {loading ? 'Optimizing...' : 'Optimize SL/TP Levels'}
          </button>
        </div>
      </div>

      {result && (
        <div className="card">
          <h3>Simulation Results</h3>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Exit Reason</div>
              <div className="stat-value" style={{ fontSize: '1rem' }}>
                {result.exit_reason}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Entry Price</div>
              <div className="stat-value">{result.entry_price.toFixed(2)}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Exit Price</div>
              <div className="stat-value">{result.exit_price.toFixed(2)}</div>
            </div>
            <div className={`stat-card ${result.profit_loss >= 0 ? 'positive' : 'negative'}`}>
              <div className="stat-label">Profit/Loss</div>
              <div className="stat-value">
                {result.profit_loss.toFixed(2)} SEK ({result.profit_loss_pct.toFixed(2)}%)
              </div>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Entry Date</div>
              <div className="stat-value" style={{ fontSize: '0.9rem' }}>{result.entry_date}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Exit Date</div>
              <div className="stat-value" style={{ fontSize: '0.9rem' }}>{result.exit_date}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Holding Days</div>
              <div className="stat-value">{result.holding_days}</div>
            </div>
            <div className={`stat-card ${result.success ? 'positive' : 'negative'}`}>
              <div className="stat-label">Result</div>
              <div className="stat-value" style={{ fontSize: '1rem' }}>
                {result.success ? '✓ Success' : '✗ Loss'}
              </div>
            </div>
          </div>

          <div className="result-item">
            <strong>Stop Loss Price:</strong> {result.stop_loss_price.toFixed(2)} ({result.stop_loss_pct}% below entry)
          </div>
          <div className="result-item">
            <strong>Take Profit Price:</strong> {result.take_profit_price.toFixed(2)} ({result.take_profit_pct}% above entry)
          </div>
        </div>
      )}

      {optimizationResult && (
        <div className="card">
          <h3>Optimization Results</h3>
          
          <div className="stats-grid">
            <div className="stat-card positive">
              <div className="stat-label">Best Stop Loss</div>
              <div className="stat-value">{optimizationResult.best_sl_pct}%</div>
            </div>
            <div className="stat-card positive">
              <div className="stat-label">Best Take Profit</div>
              <div className="stat-value">{optimizationResult.best_tp_pct}%</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Net Profit</div>
              <div className="stat-value">{optimizationResult.best_net_profit_pct.toFixed(2)}%</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Win Rate</div>
              <div className="stat-value">{optimizationResult.best_win_rate.toFixed(2)}%</div>
            </div>
          </div>

          {optimizationResult.all_results && optimizationResult.all_results.length > 0 && (
            <div style={{ marginTop: '1rem' }}>
              <h4>All Tested Combinations</h4>
              <table className="table">
                <thead>
                  <tr>
                    <th>Stop Loss %</th>
                    <th>Take Profit %</th>
                    <th>Net Profit %</th>
                    <th>Win Rate %</th>
                    <th>Total Trades</th>
                  </tr>
                </thead>
                <tbody>
                  {optimizationResult.all_results
                    .sort((a, b) => b.net_profit_pct - a.net_profit_pct)
                    .slice(0, 10)
                    .map((r, idx) => (
                      <tr key={idx}>
                        <td>{r.stop_loss_pct}%</td>
                        <td>{r.take_profit_pct}%</td>
                        <td style={{ color: r.net_profit_pct >= 0 ? 'green' : 'red' }}>
                          {r.net_profit_pct.toFixed(2)}%
                        </td>
                        <td>{r.win_rate.toFixed(2)}%</td>
                        <td>{r.total_trades}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default StopLossSimulator;
