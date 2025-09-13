import React from "react";

export default function PaymentOptions() {
  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg mt-6">
      <h2 className="text-xl font-bold mb-4 text-blue-400">💳 Payment Options</h2>
      <ul className="space-y-2">
        <li>ETH</li>
        <li>SOL</li>
        <li>BTC</li>
        <li className="text-green-400 font-bold">USDT (Stablecoin)</li>
      </ul>
    </div>
  );
}
