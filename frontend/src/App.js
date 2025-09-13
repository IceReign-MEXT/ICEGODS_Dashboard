import React, { useState } from "react";
import Login from "./components/Login";
import Subscription from "./components/Subscription";
import Dashboard from "./components/Dashboard";
import PaymentOptions from "./components/PaymentOptions";
import CryptoTicker from "./components/CryptoTicker";

function App() {
  const [user, setUser] = useState(null);
  const [subscribed, setSubscribed] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950 text-white flex justify-center p-6">
      <div className="max-w-4xl w-full">
        <h1 className="text-3xl font-bold text-center mb-6 text-cyan-400">❄️ ICEGODS Dashboard</h1>
        {!user ? (
          <Login onLogin={setUser} />
        ) : !subscribed ? (
          <Subscription onSubscribe={() => setSubscribed(true)} />
        ) : (
          <>
            <CryptoTicker />
            <Dashboard user={user} />
            <PaymentOptions />
          </>
        )}
      </div>
    </div>
  );
}

export default App;
