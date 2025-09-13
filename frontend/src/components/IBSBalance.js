import React, { useState } from "react";

export default function IBSBalance() {
  const [wallet, setWallet] = useState("");
  const [balance, setBalance] = useState(null);

  const checkBalance = async () => {
    if (!wallet) {
      alert("⚠️ Please enter a wallet address");
      return;
    }
    // For demo purposes, we fake a balance
    const fakeBalance = Math.floor(Math.random() * 1000) + " IBS";
    setBalance(fakeBalance);
  };

  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg mb-6">
      <h2 className="text-xl font-bold mb-4 text-green-400">💰 IBS Balance Checker</h2>
      <input
        type="text"
        placeholder="Enter Wallet Address"
        className="w-full p-2 rounded bg-gray-800 border border-gray-700 mb-3"
        value={wallet}
        onChange={(e) => setWallet(e.target.value)}
      />
      <button
        onClick={checkBalance}
        className="w-full bg-green-500 hover:bg-green-600 p-2 rounded font-bold"
      >
        Check Balance
      </button>
      {balance && (
        <div className="mt-4 text-lg text-white">
          Balance: <span className="font-bold">{balance}</span>
        </div>
      )}
    </div>
  );
}
