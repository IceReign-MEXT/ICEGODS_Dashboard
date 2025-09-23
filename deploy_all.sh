#!/bin/bash
# deploy_all.sh
# One command to start backend, build & deploy frontend, run bot, and check services

echo "🚀 Starting ICEGODS Dashboard deployment..."

# --- Start Backend ---
echo "🔹 Starting backend..."
cd ~/ICEGODS_Dashboard/backend || exit
if lsof -i:5003 > /dev/null; then
  echo "⚠️ Port 5003 in use, killing previous backend..."
  fuser -k 5003/tcp
fi

node server.js &
BACKEND_PID=$!
sleep 3
echo "✅ Backend running with PID $BACKEND_PID"

# --- Build Frontend ---
echo "🔹 Building frontend..."
cd ~/ICEGODS_Dashboard/frontend || exit
npm install
npm run build
if [ $? -ne 0 ]; then
  echo "❌ Frontend build failed!"
  exit 1
fi
echo "✅ Frontend built successfully"

# --- Deploy Frontend to Vercel ---
echo "🔹 Deploying frontend to Vercel..."
vercel --prod --confirm
if [ $? -ne 0 ]; then
  echo "❌ Vercel deployment failed!"
else
  echo "✅ Frontend deployed to Vercel"
fi

# --- Start Bot ---
echo "🔹 Starting Trisbo Bot..."
cd ~/ICEGODS_Dashboard/backend || exit
node bot.js &
BOT_PID=$!
sleep 2
echo "✅ Bot running with PID $BOT_PID"

# --- Check Services ---
echo "🔹 Checking backend..."
if curl -s --head http://localhost:5003 | head -n 1 | grep "200 OK" > /dev/null; then
  echo "✅ Backend is reachable at http://localhost:5003"
else
  echo "⚠️ Backend may not be reachable"
fi

echo "🔹 Checking frontend..."
FRONTEND_URL=$(vercel --prod --confirm | grep "https://")
if [ -n "$FRONTEND_URL" ]; then
  echo "✅ Frontend is live at $FRONTEND_URL"
else
  echo "⚠️ Frontend URL not detected. Check Vercel manually."
fi

echo "🎉 Deployment complete! Backend, frontend, and bot should now be running."
echo "Use CTRL+C to stop, or let it run 24/7 on your server."
