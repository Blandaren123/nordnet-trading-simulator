import React from "react";
import Portfolio from "./components/Portfolio";
import TradeSimulator from "./components/TradeSimulator";

function App() {
  return (
    <div>
      <h1>Nordnet Trading Simulator</h1>
      <Portfolio />
      <TradeSimulator />
    </div>
  );
}

export default App;
