#!/usr/bin/env python3
# backend/monitor_wallet.py
import os
import time
import json
import requests
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET", "")
MONITORED_ADDRESS = os.getenv("MONITORED_ADDRESS")  # 0x...
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# USDT contract (mainnet) - standard balanceOf interface
USDT_ADDRESS = Web3.to_checksum_address(os.getenv("USDT_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7"))
USDT_ABI = [
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"}
]

# connect
if INFURA_SECRET:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))
else:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise SystemExit("❌ Cannot connect to Infura. Check INFURA_URL / INFURA_SECRET")

usdt = w3.eth.contract(address=USDT_ADDRESS, abi=USDT_ABI)
mon_addr = Web3.to_checksum_address(MONITORED_ADDRESS)

def send_telegram(text):
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
        print("⚠️ Telegram not configured. Message:", text)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

def get_usdt_balance():
    try:
        raw = usdt.functions.balanceOf(mon_addr).call()
        decimals = usdt.functions.decimals().call()
        return raw / (10 ** decimals)
    except Exception as e:
        print("USDT balance error:", e)
        return None

def get_eth_balance():
    try:
        b = w3.eth.get_balance(mon_addr)
        return w3.from_wei(b, "ether")
    except Exception as e:
        print("ETH balance error:", e)
        return None

if __name__ == "__main__":
    print("Monitoring address:", mon_addr)
    prev_eth = None
    prev_usdt = None
    send_telegram(f"Watcher online for {mon_addr}")
    while True:
        try:
            eth = get_eth_balance()
            usdt_bal = get_usdt_balance()
            # print local log
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "ETH:", eth, "USDT:", usdt_bal)
            # notify on change
            if prev_eth is None or eth != prev_eth or usdt_bal != prev_usdt:
                msg = f"Wallet update: {mon_addr}\nETH: {eth}\nUSDT: {usdt_bal}"
                send_telegram(msg)
                prev_eth = eth
                prev_usdt = usdt_bal
        except Exception as e:
            print("Watcher error:", e)
        time.sleep(15)
