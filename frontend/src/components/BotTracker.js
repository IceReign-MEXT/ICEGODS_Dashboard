import React, { useState, useEffect } from "react";

const BotTracker = () => {
  const [bots, setBots] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/bots`)
      .then((res) => res.json())
      .then((data) => setBots(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Active Bots</h2>
      <ul>
        {bots.map((bot) => (
          <li key={bot.id}>{bot.name} - Status: {bot.status}</li>
        ))}
      </ul>
    </div>
  );
};

export default BotTracker;
