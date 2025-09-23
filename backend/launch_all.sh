#!/bin/bash
# -------------------------------
# ICEGODS Full Launch Script
# -------------------------------

# 1️⃣ Navigate to backend
cd ~/ICEGODS_Dashboard/backend

# 2️⃣ Start backend in background
echo "🚀 Starting backend on port 5003..."
PORT=5003 HOST=0.0.0.0 node server.js > backend.log 2>&1 &

# Give backend 3 seconds to start
sleep 3

# 3️⃣ Start ngrok to expose backend
echo "🔗 Starting ngrok..."
chmod +x ./ngrok
NGROK_OUTPUT=$(./ngrok http 5003 --log=stdout &)
sleep 5

# 4️⃣ Grab ngrok public URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o 'https://[a-z0-9]*\.ngrok.io')
echo "🌐 Ngrok URL: $NGROK_URL"

# 5️⃣ Update frontend .env with backend URL
cd ~/ICEGODS_Dashboard/frontend
echo "REACT_APP_BACKEND_URL=$NGROK_URL" > .env
echo "✅ Frontend .env updated with backend URL"

# 6️⃣ Build frontend
echo "🏗️ Building frontend..."
npm install
npm run build

# 7️⃣ Deploy to Vercel
echo "📦 Deploying frontend to Vercel..."
vercel --prod

echo "🎉 All done! Backend running on port 5003 and frontend deployed. Users can now interact with ICEGODS."
