import React from "react";
import ReactDOM from "react-dom";
import Subscription from "./components/Subscription";
import IBSBalance from "./components/IBSBalance";
import CryptoTicker from "./components/CryptoTicker";
import PaymentOptions from "./components/PaymentOptions";
import "./index.css";

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white p-4">
      <header className="bg-gray-900 p-4 rounded mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-blue-400">❄️ ICEGODS Dashboard</h1>
        <img src="/logo.png" alt="ICEGODS Logo" className="h-12 w-12 rounded-full border-2 border-blue-500" />
      </header>
      <main className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <CryptoTicker />
          <Subscription />
          <IBSBalance />
        </div>
        <div>
          <PaymentOptions />
        </div>
      </main>
      <footer className="bg-gray-900 p-4 mt-6 text-center text-gray-400 text-sm">
        © {new Date().getFullYear()} ICEGODS Empire
      </footer>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
