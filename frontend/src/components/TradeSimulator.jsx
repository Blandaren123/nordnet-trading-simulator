import React, { useState } from "react";

function TradeSimulator() {
  const [symbol, setSymbol] = useState("RXRX");
  const [result, setResult] = useState(null);

  const simulate = () => {
    fetch(`http://127.0.0.1:8000/simulate/${symbol}`)
      .then(res => res.json())
      .then(setResult);
  };

  return (
    <div>
      <h2>All-In Simulator</h2>
      <input value={symbol} onChange={e => setSymbol(e.target.value)} />
      <button onClick={simulate}>Simulate</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

export default TradeSimulator;
