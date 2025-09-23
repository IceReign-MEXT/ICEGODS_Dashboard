import TelegramBot from "node-telegram-bot-api";
import dotenv from "dotenv";

dotenv.config();

const token = process.env.TELEGRAM_BOT_TOKEN || "<YOUR_BOTFATHER_TOKEN>";
const bot = new TelegramBot(token, { polling: true });

bot.on("message", (msg) => {
  bot.sendMessage(msg.chat.id, "🚀 ICEGODS Bot is alive!");
});

console.log("🤖 Bot started...");
