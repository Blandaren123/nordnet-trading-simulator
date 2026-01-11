import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function RiskCalculator() {
  const [accountValue, setAccountValue] = useState('');
  const [riskPercentage, setRiskPercentage] = useState('2');
  const [entryPrice, setEntryPrice] = useState('');
  const [stopLossPrice, setStopLossPrice] = useState('');
  const [takeProfitPrice, setTakeProfitPrice] = useState('');
  
  const [positionSizeResult, setPositionSizeResult] = useState(null);
  const [riskRewardResult, setRiskRewardResult] = useState(null);
  const [error, setError] = useState('');

  const calculatePositionSize = async () => {
    setError('');
    try {
      const response = await axios.post(`${API_URL}/risk/position-size`, {
        account_value: parseFloat(accountValue),
        risk_percentage: parseFloat(riskPercentage),
        entry_price: parseFloat(entryPrice),
        stop_loss_price: parseFloat(stopLossPrice)
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setPositionSizeResult(response.data);
      }
    } catch (err) {
      setError('Failed to calculate position size: ' + err.message);
    }
  };

  const calculateRiskReward = async () => {
    setError('');
    try {
      const response = await axios.post(`${API_URL}/risk/risk-reward`, {
        entry_price: parseFloat(entryPrice),
        stop_loss_price: parseFloat(stopLossPrice),
        take_profit_price: parseFloat(takeProfitPrice)
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setRiskRewardResult(response.data);
      }
    } catch (err) {
      setError('Failed to calculate risk/reward: ' + err.message);
    }
  };

  return (
    <div>
      <div className="card">
        <h2>Risk/Reward Calculator</h2>
        <p>Calculate optimal position sizes and risk/reward ratios</p>

        {error && <div className="error">{error}</div>}

        <h3>Position Size Calculator</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Account Value (SEK)</label>
            <input
              type="number"
              value={accountValue}
              onChange={(e) => setAccountValue(e.target.value)}
              placeholder="100000"
            />
          </div>
          <div className="form-group">
            <label>Risk Percentage (%)</label>
            <input
              type="number"
              value={riskPercentage}
              onChange={(e) => setRiskPercentage(e.target.value)}
              placeholder="2"
              step="0.1"
            />
          </div>
        </div>

        <div className="form-row">
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
            <label>Stop Loss Price</label>
            <input
              type="number"
              value={stopLossPrice}
              onChange={(e) => setStopLossPrice(e.target.value)}
              placeholder="95.00"
              step="0.01"
            />
          </div>
        </div>

        <button 
          className="btn btn-primary" 
          onClick={calculatePositionSize}
          disabled={!accountValue || !riskPercentage || !entryPrice || !stopLossPrice}
        >
          Calculate Position Size
        </button>

        {positionSizeResult && (
          <div className="results">
            <h4>Position Size Results</h4>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label">Position Size</div>
                <div className="stat-value">{positionSizeResult.position_size.toFixed(2)} shares</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Total Cost</div>
                <div className="stat-value">{positionSizeResult.total_cost.toFixed(2)} SEK</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Risk Amount</div>
                <div className="stat-value">{positionSizeResult.risk_amount.toFixed(2)} SEK</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Risk Per Share</div>
                <div className="stat-value">{positionSizeResult.risk_per_share.toFixed(2)} SEK</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3>Risk/Reward Ratio Calculator</h3>
        
        <div className="form-row">
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
            <label>Stop Loss Price</label>
            <input
              type="number"
              value={stopLossPrice}
              onChange={(e) => setStopLossPrice(e.target.value)}
              placeholder="95.00"
              step="0.01"
            />
          </div>
          <div className="form-group">
            <label>Take Profit Price</label>
            <input
              type="number"
              value={takeProfitPrice}
              onChange={(e) => setTakeProfitPrice(e.target.value)}
              placeholder="110.00"
              step="0.01"
            />
          </div>
        </div>

        <button 
          className="btn btn-primary" 
          onClick={calculateRiskReward}
          disabled={!entryPrice || !stopLossPrice || !takeProfitPrice}
        >
          Calculate Risk/Reward
        </button>

        {riskRewardResult && (
          <div className="results">
            <h4>Risk/Reward Results</h4>
            <div className="stats-grid">
              <div className="stat-card negative">
                <div className="stat-label">Risk</div>
                <div className="stat-value">{riskRewardResult.risk.toFixed(2)} ({riskRewardResult.risk_pct.toFixed(2)}%)</div>
              </div>
              <div className="stat-card positive">
                <div className="stat-label">Reward</div>
                <div className="stat-value">{riskRewardResult.reward.toFixed(2)} ({riskRewardResult.reward_pct.toFixed(2)}%)</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Risk/Reward Ratio</div>
                <div className="stat-value">1:{riskRewardResult.risk_reward_ratio.toFixed(2)}</div>
              </div>
            </div>
            <div className="result-item">
              <strong>Recommendation:</strong> A risk/reward ratio of at least 1:2 or higher is generally considered favorable for most trading strategies.
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3>Risk Management Tips</h3>
        <ul style={{ paddingLeft: '1.5rem', color: '#6b7280', lineHeight: '2' }}>
          <li>Never risk more than 1-2% of your account on a single trade</li>
          <li>Aim for a risk/reward ratio of at least 1:2</li>
          <li>Always use stop losses to protect your capital</li>
          <li>Position size should be based on your stop loss distance, not on how much you want to buy</li>
          <li>Diversify across multiple positions to reduce overall portfolio risk</li>
        </ul>
      </div>
    </div>
  );
}

export default RiskCalculator;
