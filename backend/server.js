import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import fetch from "node-fetch";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// -------------------------
// Example endpoints
// -------------------------

// Health check
app.get("/", (req, res) => {
  res.send("🚀 ICEGODS Backend Running!");
});

// Get ETH balance (mock example)
app.get("/balance/eth/:address", async (req, res) => {
  const address = req.params.address;
  // TODO: connect real Ethereum API (Infura/Etherscan)
  res.json({ address, balance: Math.floor(Math.random() * 10) + " ETH" });
});

// Telegram test message
app.get("/notify", async (req, res) => {
  const chatId = process.env.TELEGRAM_CHAT_ID;
  const token = process.env.TELEGRAM_TOKEN;
  try {
    await fetch(`https://api.telegram.org/bot${token}/sendMessage?chat_id=${chatId}&text=Hello from ICEGODS Backend`);
    res.json({ success: true });
  } catch (err) {
    res.json({ success: false, error: err.message });
  }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Backend running on http://localhost:${PORT}`));
