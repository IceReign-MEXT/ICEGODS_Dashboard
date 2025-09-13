import React from "react";
import ReactDOM from "react-dom";
import Subscription from "./components/Subscription";
import IBSBalance from "./components/IBSBalance";
import BotTracker from "./components/BotTracker";
import PaymentOptions from "./components/PaymentOptions";
import CryptoTicker from "./components/CryptoTicker";
import ParticlesBackground from "./components/ParticlesBackground";
import "./index.css";

function App() {
  return (
    <div className="min-h-screen text-white relative">
      {/* Particles Background */}
      <ParticlesBackground />

      {/* Header */}
      <header className="bg-gradient-to-r from-cyan-500 to-blue-500 shadow-lg p-4 flex items-center justify-between">
        <h1 className="text-3xl font-extrabold drop-shadow-lg">❄️ ICEGODS Dashboard</h1>
        <img
          src="/logo.png"
          alt="ICEGODS Logo"
          className="h-12 w-12 rounded-full border-2 border-white"
        />
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Column */}
        <div>
          <CryptoTicker /> {/* Live crypto ticker */}
          <Subscription />
          <IBSBalance />
        </div>

        {/* Right Column */}
        <div>
          <BotTracker />
          <PaymentOptions />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 p-4 text-center text-gray-400 text-sm mt-10">
        © {new Date().getFullYear()} ICEGODS Empire. All rights reserved.
      </footer>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
