#!/usr/bin/env python3
# monitor_testnet.py  — ETH + ERC-20 monitor for testnets (sepolia)
import os, time, requests
from web3 import Web3
from dotenv import load_dotenv
load_dotenv(".env.test")

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET", "")
MONITORED_ADDRESS = os.getenv("MONITORED_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")

if INFURA_SECRET:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))
else:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise SystemExit("❌ Cannot connect to RPC. Check INFURA_URL/INFURA_SECRET")

MON = Web3.to_checksum_address(MONITORED_ADDRESS)
print("Monitoring:", MON)
# Minimal ERC-20 ABI for balanceOf + decimals
ERC20_ABI = [
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}
]

token_contract = None
decimals = 18
if TOKEN_ADDRESS:
    token_contract = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=ERC20_ABI)
    try:
        decimals = token_contract.functions.decimals().call()
    except Exception:
        decimals = 18

def send_telegram(text: str):
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
        print("Telegram not configured. Message:", text)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=6)
    except Exception as e:
        print("Telegram send error:", e)

def get_eth_balance(addr):
    try:
        b = w3.eth.get_balance(addr)
        return w3.from_wei(b, "ether")
    except Exception as e:
        print("ETH balance error:", e)
        return None

def get_token_balance(addr):
    if not token_contract:
        return None
    try:
        raw = token_contract.functions.balanceOf(addr).call()
        return raw / (10 ** decimals)
    except Exception as e:
        print("Token balance error:", e)
        return None

def main(poll_interval=15):
    prev_eth = None
    prev_token = None
    send_telegram(f"Monitor started for {MON}\nNetwork: {INFURA_URL}")
    while True:
        eth = get_eth_balance(MON)
        tok = get_token_balance(MON)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "ETH:", eth, "TOKEN:", tok)
        # Notify only on change
        if prev_eth is None or eth != prev_eth or tok != prev_token:
            msg = f"Wallet update: {MON}\nETH: {eth}\nToken: {tok}"
            send_telegram(msg)
            prev_eth, prev_token = eth, tok
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
