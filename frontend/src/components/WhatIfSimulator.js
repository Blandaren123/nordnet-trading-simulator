import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function WhatIfSimulator() {
  const [symbol, setSymbol] = useState('');
  const [investmentAmount, setInvestmentAmount] = useState('100000');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [result, setResult] = useState(null);
  const [compareSymbols, setCompareSymbols] = useState('');
  const [compareResult, setCompareResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const simulateAllIn = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/whatif/all-in`, {
        symbol,
        investment_amount: parseFloat(investmentAmount),
        start_date: startDate,
        end_date: endDate
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError('Failed to simulate: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const compareScenarios = async () => {
    setLoading(true);
    setError('');
    setCompareResult(null);

    try {
      const symbols = compareSymbols.split(',').map(s => s.trim().toUpperCase());
      
      const response = await axios.post(`${API_URL}/whatif/compare`, {
        symbols,
        investment_amount: parseFloat(investmentAmount),
        start_date: startDate,
        end_date: endDate
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setCompareResult(response.data);
      }
    } catch (err) {
      setError('Failed to compare: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h2>What-If Simulator 🚀</h2>
        <p>"What if I all-in RXRX / IonQ?" - Find out here!</p>

        {error && <div className="error">{error}</div>}

        <h3>Single Stock All-In Scenario</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Symbol (e.g., RXRX, IONQ, AAPL)</label>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="RXRX"
            />
          </div>
          <div className="form-group">
            <label>Investment Amount (SEK)</label>
            <input
              type="number"
              value={investmentAmount}
              onChange={(e) => setInvestmentAmount(e.target.value)}
              placeholder="100000"
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
            <label>End Date (optional - defaults to today)</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>

        <button 
          className="btn btn-primary" 
          onClick={simulateAllIn}
          disabled={loading || !symbol || !investmentAmount || !startDate}
        >
          {loading ? 'Simulating...' : 'Simulate All-In Scenario'}
        </button>
      </div>

      {result && (
        <div className="card">
          <h3>All-In Results: {result.symbol}</h3>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Initial Investment</div>
              <div className="stat-value">{result.investment_amount.toLocaleString()} SEK</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Final Value</div>
              <div className="stat-value">{result.exit_value.toLocaleString()} SEK</div>
            </div>
            <div className={`stat-card ${result.profit_loss >= 0 ? 'positive' : 'negative'}`}>
              <div className="stat-label">Profit/Loss</div>
              <div className="stat-value">
                {result.profit_loss.toLocaleString()} SEK
              </div>
            </div>
            <div className={`stat-card ${result.profit_loss_pct >= 0 ? 'positive' : 'negative'}`}>
              <div className="stat-label">Return</div>
              <div className="stat-value">{result.profit_loss_pct.toFixed(2)}%</div>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Entry Price</div>
              <div className="stat-value">{result.entry_price.toFixed(2)}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Exit Price</div>
              <div className="stat-value">{result.exit_price.toFixed(2)}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Shares Purchased</div>
              <div className="stat-value">{result.shares.toFixed(2)}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Holding Period</div>
              <div className="stat-value">{result.holding_days} days</div>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card positive">
              <div className="stat-label">Peak Value</div>
              <div className="stat-value">{result.peak_value.toLocaleString()} SEK</div>
              <div style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>{result.peak_date}</div>
            </div>
            <div className="stat-card negative">
              <div className="stat-label">Max Drawdown</div>
              <div className="stat-value">{result.max_drawdown_pct.toFixed(2)}%</div>
              <div style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>{result.max_drawdown_date}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Annualized Return</div>
              <div className="stat-value">{result.annualized_return.toFixed(2)}%</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Annual Volatility</div>
              <div className="stat-value">{result.annual_volatility_pct.toFixed(2)}%</div>
            </div>
          </div>

          {result.timeline && result.timeline.length > 0 && (
            <div style={{ marginTop: '2rem' }}>
              <h4>Portfolio Value Over Time</h4>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={result.timeline}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={(date) => new Date(date).toLocaleDateString()}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(date) => new Date(date).toLocaleDateString()}
                    formatter={(value) => value.toLocaleString()}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="portfolio_value" 
                    stroke="#667eea" 
                    strokeWidth={2}
                    name="Portfolio Value (SEK)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <h3>Compare Multiple Stocks</h3>
        <p>Enter multiple stock symbols separated by commas</p>

        <div className="form-group">
          <label>Symbols (comma-separated)</label>
          <input
            type="text"
            value={compareSymbols}
            onChange={(e) => setCompareSymbols(e.target.value.toUpperCase())}
            placeholder="RXRX, IONQ, AAPL, TSLA"
          />
        </div>

        <button 
          className="btn btn-primary" 
          onClick={compareScenarios}
          disabled={loading || !compareSymbols || !investmentAmount || !startDate}
        >
          {loading ? 'Comparing...' : 'Compare All-In Scenarios'}
        </button>
      </div>

      {compareResult && (
        <div className="card">
          <h3>Comparison Results</h3>

          <div className="stats-grid">
            <div className="stat-card positive">
              <div className="stat-label">Best Performer</div>
              <div className="stat-value" style={{ fontSize: '1.2rem' }}>
                {compareResult.best_performer.symbol}
              </div>
              <div style={{ fontSize: '0.9rem', marginTop: '0.25rem' }}>
                {compareResult.best_performer.return_pct.toFixed(2)}% return
              </div>
            </div>
            <div className="stat-card negative">
              <div className="stat-label">Worst Performer</div>
              <div className="stat-value" style={{ fontSize: '1.2rem' }}>
                {compareResult.worst_performer.symbol}
              </div>
              <div style={{ fontSize: '0.9rem', marginTop: '0.25rem' }}>
                {compareResult.worst_performer.return_pct.toFixed(2)}% return
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Performance Spread</div>
              <div className="stat-value">{compareResult.spread.toFixed(2)}%</div>
            </div>
          </div>

          {compareResult.scenarios && compareResult.scenarios.length > 0 && (
            <div style={{ marginTop: '2rem' }}>
              <h4>Performance Comparison</h4>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={compareResult.scenarios}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="symbol" />
                  <YAxis />
                  <Tooltip formatter={(value) => `${value.toFixed(2)}%`} />
                  <Legend />
                  <Bar dataKey="profit_loss_pct" fill="#667eea" name="Return %" />
                </BarChart>
              </ResponsiveContainer>

              <table className="table" style={{ marginTop: '1rem' }}>
                <thead>
                  <tr>
                    <th>Symbol</th>
                    <th>Final Value</th>
                    <th>Profit/Loss</th>
                    <th>Return %</th>
                    <th>Max Drawdown %</th>
                    <th>Volatility %</th>
                  </tr>
                </thead>
                <tbody>
                  {compareResult.scenarios
                    .sort((a, b) => b.profit_loss_pct - a.profit_loss_pct)
                    .map((scenario, idx) => (
                      <tr key={idx}>
                        <td><strong>{scenario.symbol}</strong></td>
                        <td>{scenario.exit_value.toLocaleString()} SEK</td>
                        <td style={{ color: scenario.profit_loss >= 0 ? 'green' : 'red' }}>
                          {scenario.profit_loss.toLocaleString()} SEK
                        </td>
                        <td style={{ color: scenario.profit_loss_pct >= 0 ? 'green' : 'red' }}>
                          {scenario.profit_loss_pct.toFixed(2)}%
                        </td>
                        <td>{scenario.max_drawdown_pct.toFixed(2)}%</td>
                        <td>{scenario.annual_volatility_pct.toFixed(2)}%</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <div className="card">
        <h3>⚠️ Disclaimer</h3>
        <p style={{ color: '#6b7280', lineHeight: '1.8' }}>
          This simulator is for educational and entertainment purposes only. Going "all-in" on any single stock 
          is extremely risky and not recommended for actual investing. Past performance does not guarantee 
          future results. Always diversify your portfolio and never invest more than you can afford to lose.
        </p>
      </div>
    </div>
  );
}

export default WhatIfSimulator;
