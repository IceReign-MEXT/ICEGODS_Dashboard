#!/bin/bash

# --- Step 1: Start backend ---
echo "🚀 Starting backend on port 5003..."
cd ~/ICEGODS_Dashboard/backend
PORT=5003 HOST=0.0.0.0 node server.js &
BACKEND_PID=$!
sleep 5
echo "✅ Backend started with PID $BACKEND_PID"

# --- Step 2: Start ngrok for public URL ---
if ! command -v ngrok &> /dev/null
then
    echo "⚠️ ngrok not found, skipping tunnel. Add your ngrok authtoken to use."
    NGROK_URL="http://localhost:5003"
else
    echo "🔹 Starting ngrok tunnel..."
    NGROK_OUTPUT=$(ngrok http 5003 --log=stdout &)
    sleep 5
    NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')
    echo "✅ ngrok URL: $NGROK_URL"
fi

# --- Step 3: Update frontend .env ---
echo "🔹 Updating frontend .env with backend URL..."
cd ~/ICEGODS_Dashboard/frontend
echo "REACT_APP_BACKEND_URL=$NGROK_URL" > .env

# --- Step 4: Build frontend ---
echo "📦 Building frontend..."
npm run build

# --- Step 5: Start frontend server ---
echo "🚀 Starting frontend..."
npm start &
FRONTEND_PID=$!
sleep 5
echo "✅ Frontend started with PID $FRONTEND_PID"

# --- Step 6: Launch Bot ---
echo "🤖 Launching Trisbo Bot..."
cd ~/ICEGODS_Dashboard/backend
node bot.js &
BOT_PID=$!
sleep 2
echo "✅ Bot started with PID $BOT_PID"

# --- Step 7: Done ---
echo "🎉 All done!"
echo "Backend URL: $NGROK_URL"
echo "Frontend running locally at: http://localhost:3000"
echo "Bot is live and monitoring"
