import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Portfolio() {
  const [portfolioId] = useState('default');
  const [symbol, setSymbol] = useState('');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [summary, setSummary] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadSummary = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/portfolio/${portfolioId}/summary`);
      setSummary(response.data);
      setError('');
    } catch (err) {
      // Portfolio might not exist yet
      console.log('Portfolio not found, create one first');
    }
  }, [portfolioId]);

  const loadTransactions = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/portfolio/${portfolioId}/transactions`);
      setTransactions(response.data.transactions);
    } catch (err) {
      console.log('No transactions yet');
    }
  }, [portfolioId]);

  useEffect(() => {
    loadSummary();
    loadTransactions();
  }, [loadSummary, loadTransactions]);

  const createPortfolio = async () => {
    try {
      await axios.post(`${API_URL}/portfolio/create`, {
        portfolio_id: portfolioId,
        initial_cash: 100000
      });
      setMessage('Portfolio created successfully!');
      loadSummary();
    } catch (err) {
      setError('Failed to create portfolio');
    }
  };

  const buyStock = async () => {
    try {
      const response = await axios.post(`${API_URL}/portfolio/${portfolioId}/buy`, {
        symbol,
        quantity: parseFloat(quantity),
        price: parseFloat(price)
      });
      
      if (response.data.success) {
        setMessage('Buy order executed successfully!');
        setSymbol('');
        setQuantity('');
        setPrice('');
        loadSummary();
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError('Failed to execute buy order');
    }
  };

  const sellStock = async () => {
    try {
      const response = await axios.post(`${API_URL}/portfolio/${portfolioId}/sell`, {
        symbol,
        quantity: parseFloat(quantity),
        price: parseFloat(price)
      });
      
      if (response.data.success) {
        setMessage('Sell order executed successfully!');
        setSymbol('');
        setQuantity('');
        setPrice('');
        loadSummary();
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError('Failed to execute sell order');
    }
  };

  return (
    <div>
      <div className="card">
        <h2>Portfolio Tracker</h2>
        
        {message && <div className="success">{message}</div>}
        {error && <div className="error">{error}</div>}

        {!summary && (
          <div>
            <p>No portfolio found. Create one to get started.</p>
            <button className="btn btn-primary" onClick={createPortfolio}>
              Create Portfolio (100,000 SEK)
            </button>
          </div>
        )}

        {summary && (
          <div>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label">Total Value</div>
                <div className="stat-value">{summary.total_value.toFixed(2)} SEK</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Cash</div>
                <div className="stat-value">{summary.cash.toFixed(2)} SEK</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Invested Value</div>
                <div className="stat-value">{summary.invested_value.toFixed(2)} SEK</div>
              </div>
              <div className={`stat-card ${summary.total_return >= 0 ? 'positive' : 'negative'}`}>
                <div className="stat-label">Total Return</div>
                <div className="stat-value">{summary.total_return.toFixed(2)}%</div>
              </div>
            </div>

            <h3>Current Positions</h3>
            {Object.keys(summary.positions).length > 0 ? (
              <table className="table">
                <thead>
                  <tr>
                    <th>Symbol</th>
                    <th>Quantity</th>
                    <th>Avg Price</th>
                    <th>Current Price</th>
                    <th>Value</th>
                    <th>Gain/Loss</th>
                    <th>Return %</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(summary.positions).map(([sym, pos]) => (
                    <tr key={sym}>
                      <td><strong>{sym}</strong></td>
                      <td>{pos.quantity.toFixed(2)}</td>
                      <td>{pos.avg_price.toFixed(2)}</td>
                      <td>{pos.current_price.toFixed(2)}</td>
                      <td>{pos.value.toFixed(2)} SEK</td>
                      <td style={{ color: pos.gain >= 0 ? 'green' : 'red' }}>
                        {pos.gain.toFixed(2)} SEK
                      </td>
                      <td style={{ color: pos.gain_pct >= 0 ? 'green' : 'red' }}>
                        {pos.gain_pct.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No positions yet. Buy some stocks to get started!</p>
            )}
          </div>
        )}
      </div>

      <div className="card">
        <h3>Trade Stocks</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Symbol</label>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="AAPL, TSLA, etc."
            />
          </div>
          <div className="form-group">
            <label>Quantity</label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder="10"
            />
          </div>
          <div className="form-group">
            <label>Price per Share</label>
            <input
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              placeholder="150.00"
            />
          </div>
        </div>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button className="btn btn-success" onClick={buyStock}>
            Buy
          </button>
          <button className="btn btn-danger" onClick={sellStock}>
            Sell
          </button>
          <button className="btn btn-secondary" onClick={loadSummary}>
            Refresh
          </button>
        </div>
      </div>

      {transactions.length > 0 && (
        <div className="card">
          <h3>Transaction History</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {transactions.slice().reverse().map((t, idx) => (
                <tr key={idx}>
                  <td>
                    <span style={{ 
                      color: t.type === 'BUY' ? 'green' : 'red',
                      fontWeight: 'bold'
                    }}>
                      {t.type}
                    </span>
                  </td>
                  <td>{t.symbol}</td>
                  <td>{t.quantity.toFixed(2)}</td>
                  <td>{t.price.toFixed(2)}</td>
                  <td>{t.total.toFixed(2)} SEK</td>
                  <td>{new Date(t.date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Portfolio;
