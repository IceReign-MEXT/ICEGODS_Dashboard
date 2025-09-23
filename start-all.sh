#!/bin/bash
cd ~/ICEGODS_Dashboard/backend
pm2 start server.js --name icegods-backend

cd ~/ICEGODS_Dashboard/frontend
pm2 start "serve -s build -l 3000" --name icegods-frontend

cd ~/ICEGODS_Dashboard/frontend
pm2 start bot.js --name icegods-bot

pm2 save
pm2 ls
