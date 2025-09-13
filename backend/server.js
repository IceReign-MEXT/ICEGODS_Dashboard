import express from "express";
import cors from "cors";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Telegram notification
app.post("/api/notify", async (req, res) => {
  const { chatId, message } = req.body;
  try {
    const url = `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`;
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text: message }),
    });
    const data = await resp.json();
    res.json({ success: data.ok });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ETH balance check
app.get("/api/balance/eth/:wallet", async (req, res) => {
  const wallet = req.params.wallet;
  // For simplicity: return fake balance
  const balance = (Math.random() * 10).toFixed(4) + " ETH";
  res.json({ wallet, balance });
});

app.listen(PORT, () => {
  console.log(`🚀 Backend running on http://localhost:${PORT}`);
});
