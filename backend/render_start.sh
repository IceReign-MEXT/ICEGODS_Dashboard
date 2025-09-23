#!/bin/bash

# --- Step 1: Start backend on Render port ---
echo "🚀 Starting backend..."
cd ~/ICEGODS_Dashboard/backend
PORT=${PORT:-10000} node server.js &
BACKEND_PID=$!
sleep 5
echo "✅ Backend started with PID $BACKEND_PID on port $PORT"

# --- Step 2: Update frontend .env for Render ---
cd ~/ICEGODS_Dashboard/frontend
echo "REACT_APP_BACKEND_URL=https://your-backend.onrender.com" > .env
echo "REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_51Rr7VNLYSXrPeABJEaBUl7zmFlBHD4iukl8BQqhKODw38IELndfOe709q7CStlEK6TxvI8RewhFcgJYF5Lv5rH7e00I61988W2" >> .env

# --- Step 3: Build frontend for deployment ---
echo "📦 Building frontend..."
npm run build

# --- Step 4: Start frontend server ---
echo "🚀 Starting frontend on Render port..."
npm start &
FRONTEND_PID=$!
sleep 5
echo "✅ Frontend started with PID $FRONTEND_PID"

# --- Step 5: Launch Bot ---
echo "🤖 Launching Trisbo Bot..."
cd ~/ICEGODS_Dashboard/backend
node bot.js &
BOT_PID=$!
sleep 2
echo "✅ Bot started with PID $BOT_PID"

# --- Step 6: Done ---
echo "🎉 Render deployment ready!"
echo "Backend URL: https://your-backend.onrender.com"
echo "Frontend URL: https://your-frontend.onrender.com"
echo "Bot is live and monitoring"
