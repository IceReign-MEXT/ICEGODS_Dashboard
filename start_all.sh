#!/bin/bash
# =============================
# ICEGODS Dashboard Full Launcher
# =============================

# --- Navigate to backend ---
cd ~/ICEGODS_Dashboard/backend || exit

echo "🚀 Starting Backend..."
# Kill previous instance if port 5003 is in use
fuser -k 5003/tcp >/dev/null 2>&1
# Start backend
nohup node server.js > backend.log 2>&1 &

sleep 3

echo "🔹 Backend should be running at http://localhost:5003"

# --- Start Bot ---
echo "🤖 Starting Telegram Bot..."
nohup node bot.js > bot.log 2>&1 &

sleep 2

echo "🔹 Bot should be running now"

# --- Start Frontend ---
cd ~/ICEGODS_Dashboard/frontend || exit

echo "🌐 Starting Frontend..."
# If you haven’t installed serve yet
npm install serve >/dev/null 2>&1
nohup serve -s build -l 3000 > frontend.log 2>&1 &

sleep 2

echo "🔹 Frontend running at http://localhost:3000"

echo "🎉 All services are running. Check your Telegram bot and frontend now!"
