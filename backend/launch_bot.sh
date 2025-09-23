#!/bin/bash
# -------------------------------
# ICEGODS Full Launch Script
# -------------------------------

# 1️⃣ Navigate to backend
cd ~/ICEGODS_Dashboard/backend

# 2️⃣ Kill any old node processes
echo "🛑 Killing old backend processes..."
pkill -f "node server.js"

# 3️⃣ Start backend in background
echo "🚀 Starting backend on port 5003..."
PORT=5003 HOST=0.0.0.0 node server.js > backend.log 2>&1 &
sleep 5

# 4️⃣ Start ngrok to expose backend publicly
echo "🔗 Starting ngrok..."
chmod +x ./ngrok
./ngrok http 5003 > ngrok.log 2>&1 &
sleep 5

# 5️⃣ Grab ngrok public URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o 'https://[a-z0-9]*\.ngrok.io')
echo "🌐 Ngrok URL: $NGROK_URL"

# 6️⃣ Update frontend .env with backend URL
cd ~/ICEGODS_Dashboard/frontend
echo "REACT_APP_BACKEND_URL=$NGROK_URL" > .env
echo "✅ Frontend .env updated with backend URL"

# 7️⃣ Install frontend dependencies (if missing)
npm install

# 8️⃣ Build frontend
echo "🏗️ Building frontend..."
npm run build

# 9️⃣ Deploy frontend to Vercel
echo "📦 Deploying frontend to Vercel..."
vercel --prod

# 1️⃣0️⃣ Start the bot monitoring (optional)
cd ~/ICEGODS_Dashboard/backend
echo "🤖 Starting Trisbo Bot..."
nohup node Trisbo_Bot/server.js > bot.log 2>&1 &

echo "🎉 All done! Backend, frontend, and bot are running. Users can now interact and subscribe."
