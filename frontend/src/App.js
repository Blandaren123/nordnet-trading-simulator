import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Portfolio from './components/Portfolio';
import Backtesting from './components/Backtesting';
import RiskCalculator from './components/RiskCalculator';
import StopLossSimulator from './components/StopLossSimulator';
import WhatIfSimulator from './components/WhatIfSimulator';
import Home from './components/Home';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-brand">
            <h1>📈 Nordnet Trading Simulator</h1>
          </div>
          <ul className="nav-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/portfolio">Portfolio</Link></li>
            <li><Link to="/backtesting">Backtesting</Link></li>
            <li><Link to="/risk-calculator">Risk Calculator</Link></li>
            <li><Link to="/stop-loss">Stop Loss/TP</Link></li>
            <li><Link to="/what-if">What-If Simulator</Link></li>
          </ul>
        </nav>

        <div className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/backtesting" element={<Backtesting />} />
            <Route path="/risk-calculator" element={<RiskCalculator />} />
            <Route path="/stop-loss" element={<StopLossSimulator />} />
            <Route path="/what-if" element={<WhatIfSimulator />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
