import React, { useState, useEffect } from "react";

function Portfolio() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div>
      <h2>Portfolio</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default Portfolio;
