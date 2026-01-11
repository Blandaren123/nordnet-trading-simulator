import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [portfolio, setPortfolio] = useState({ cash: 0, positions: [] });
  const [symbol, setSymbol] = useState('');
  const [quantity, setQuantity] = useState('');
  const [history, setHistory] = useState([]);

  const fetchPortfolio = async () => {
    try {
      const response = await axios.get('/portfolio');
      setPortfolio(response.data);
    } catch (error) {
      console.error('Error fetching portfolio:', error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/history');
      setHistory(response.data.trades);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  useEffect(() => {
    fetchPortfolio();
    fetchHistory();
  }, []);

  const handleTrade = async (action) => {
    if (!symbol || !quantity) {
      alert('Please enter symbol and quantity');
      return;
    }

    try {
      const response = await axios.post('/trade', {
        symbol: symbol.toUpperCase(),
        quantity: parseInt(quantity),
        action: action
      });

      if (response.data.error) {
        alert(response.data.error);
      } else {
        alert(`Trade executed successfully!`);
        setSymbol('');
        setQuantity('');
        fetchPortfolio();
        fetchHistory();
      }
    } catch (error) {
      console.error('Error executing trade:', error);
      alert('Error executing trade');
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Nordnet Trading Simulator</h1>
      </header>

      <div className="container">
        <div className="card">
          <h2>Portfolio</h2>
          <div className="cash">
            <strong>Cash:</strong> ${portfolio.cash.toFixed(2)}
          </div>
          <h3>Positions</h3>
          {portfolio.positions.length === 0 ? (
            <p>No positions</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Quantity</th>
                  <th>Avg Price</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.positions.map((pos) => (
                  <tr key={pos.symbol}>
                    <td>{pos.symbol}</td>
                    <td>{pos.quantity}</td>
                    <td>${pos.avg_price.toFixed(2)}</td>
                    <td>${(pos.quantity * pos.avg_price).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="card">
          <h2>Execute Trade</h2>
          <div className="form">
            <input
              type="text"
              placeholder="Stock Symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
            />
            <input
              type="number"
              placeholder="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
            <div className="buttons">
              <button className="buy-btn" onClick={() => handleTrade('buy')}>
                Buy
              </button>
              <button className="sell-btn" onClick={() => handleTrade('sell')}>
                Sell
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Trade History</h2>
          {history.length === 0 ? (
            <p>No trades yet</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Action</th>
                  <th>Symbol</th>
                  <th>Quantity</th>
                  <th>Price</th>
                </tr>
              </thead>
              <tbody>
                {history.slice().reverse().map((trade, idx) => (
                  <tr key={idx}>
                    <td>{new Date(trade.timestamp).toLocaleString()}</td>
                    <td className={trade.action}>{trade.action.toUpperCase()}</td>
                    <td>{trade.symbol}</td>
                    <td>{trade.quantity}</td>
                    <td>${trade.price.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
