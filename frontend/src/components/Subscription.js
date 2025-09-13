import React, { useState } from "react";

export default function Subscription() {
  const [name, setName] = useState("");
  const [plan, setPlan] = useState("");
  const [txHash, setTxHash] = useState("");

  const plans = [
    { label: "Hourly - 0.001 ETH", value: "hourly" },
    { label: "Weekly - 0.01 ETH", value: "weekly" },
    { label: "Monthly - 0.05 ETH", value: "monthly" },
    { label: "Yearly - 0.5 ETH", value: "yearly" },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`✅ Subscription submitted!\nName: ${name}\nPlan: ${plan}\nTx: ${txHash}`);
  };

  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg mb-6">
      <h2 className="text-xl font-bold mb-4 text-cyan-400">💳 Subscribe to ICEGODS Dashboard</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Your Name"
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <select
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
          value={plan}
          onChange={(e) => setPlan(e.target.value)}
        >
          <option value="">Select Plan</option>
          {plans.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Transaction Hash"
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
          value={txHash}
          onChange={(e) => setTxHash(e.target.value)}
        />
        <button type="submit" className="w-full bg-cyan-500 hover:bg-cyan-600 p-2 rounded font-bold">
          Subscribe
        </button>
      </form>
    </div>
  );
}
