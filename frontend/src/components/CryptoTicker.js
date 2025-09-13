import React, { useEffect, useState } from "react";

export default function CryptoTicker() {
  const [prices, setPrices] = useState({});

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const resp = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,solana&vs_currencies=usd");
        const data = await resp.json();
        setPrices(data);
      } catch (err) {}
    };
    fetchPrices();
    const interval = setInterval(fetchPrices, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg mb-6">
      <h2 className="text-xl font-bold mb-4 text-yellow-400">📈 Crypto Prices</h2>
      <ul className="space-y-2">
        <li>BTC: ${prices.bitcoin?.usd}</li>
        <li>ETH: ${prices.ethereum?.usd}</li>
        <li>SOL: ${prices.solana?.usd}</li>
      </ul>
    </div>
  );
}


