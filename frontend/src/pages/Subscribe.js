import React, { useState } from "react";
import axios from "axios";

const Subscribe = () => {
  const [user, setUser] = useState("");
  const [plan, setPlan] = useState("monthly");
  const [txHash, setTxHash] = useState("");
  const [status, setStatus] = useState("");

  const handleSubscribe = async () => {
    if (!user || !plan || !txHash) {
      setStatus("❌ All fields are required");
      return;
    }

    try {
      const res = await axios.post("http://127.0.0.1:5000/subscribe", {
        user,
        plan,
        tx_hash: txHash,
      });

      if (res.data.status === "success") {
        setStatus(`✅ Subscription successful: ${res.data.plan}`);
      } else {
        setStatus(`❌ Failed: ${res.data.reason}`);
      }
    } catch (err) {
      console.error(err);
      setStatus("❌ Error connecting to backend");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "500px", margin: "auto" }}>
      <h1>Subscribe to ICEGODS Dashboard</h1>
      <input
        type="text"
        placeholder="Your Name"
        value={user}
        onChange={(e) => setUser(e.target.value)}
        style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
      />
      <select
        value={plan}
        onChange={(e) => setPlan(e.target.value)}
        style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
      >
        <option value="monthly">Monthly - 0.01 ETH</option>
        <option value="yearly">Yearly - 0.10 ETH</option>
        <option value="lifetime">Lifetime - 0.25 ETH</option>
      </select>
      <input
        type="text"
        placeholder="Transaction Hash"
        value={txHash}
        onChange={(e) => setTxHash(e.target.value)}
        style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
      />
      <button
        onClick={handleSubscribe}
        style={{ padding: "0.5rem 1rem", width: "100%" }}
      >
        Subscribe
      </button>
      <p style={{ marginTop: "1rem" }}>{status}</p>
    </div>
  );
};

export default Subscribe;
