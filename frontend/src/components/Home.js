import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div>
      <div className="card">
        <h2>Welcome to Nordnet Trading Simulator 🚀</h2>
        <p style={{ fontSize: '1.1rem', color: '#6b7280', marginBottom: '2rem' }}>
          A comprehensive trading and investing tool for backtesting, risk analysis, and portfolio tracking.
        </p>
      </div>

      <div className="feature-grid">
        <Link to="/portfolio" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="feature-card">
            <h3>📊 Portfolio Tracker</h3>
            <p>Track your investments, monitor performance, and view detailed position analytics with real-time updates.</p>
          </div>
        </Link>

        <Link to="/backtesting" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="feature-card">
            <h3>⏮️ Backtesting</h3>
            <p>Test trading strategies on historical data. Includes buy-and-hold and SMA crossover strategies.</p>
          </div>
        </Link>

        <Link to="/risk-calculator" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="feature-card">
            <h3>⚖️ Risk/Reward Calculator</h3>
            <p>Calculate position sizes, risk/reward ratios, and optimize your trade parameters for better risk management.</p>
          </div>
        </Link>

        <Link to="/stop-loss" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="feature-card">
            <h3>🎯 Stop Loss/Take Profit</h3>
            <p>Simulate trades with stop loss and take profit levels. Optimize your exit strategies.</p>
          </div>
        </Link>

        <Link to="/what-if" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div className="feature-card">
            <h3>🤔 What-If Simulator</h3>
            <p>"What if I all-in RXRX / IonQ?" - Simulate extreme scenarios, compare strategies, and explore DCA vs lump sum.</p>
          </div>
        </Link>
      </div>

      <div className="card">
        <h3>Getting Started</h3>
        <ol style={{ paddingLeft: '1.5rem', color: '#6b7280', lineHeight: '2' }}>
          <li>Start by creating a portfolio and adding some trades</li>
          <li>Run backtests on your favorite stocks to see historical performance</li>
          <li>Use the risk calculator to determine optimal position sizing</li>
          <li>Experiment with the what-if simulator to explore different scenarios</li>
        </ol>
      </div>
    </div>
  );
}

export default Home;
