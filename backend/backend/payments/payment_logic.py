# backend/payments/payment_logic.py

import os
import sqlite3
from datetime import datetime, timedelta
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv("backend/config/config.env")

INFURA_URL = os.getenv("INFURA_URL")
PAYMENT_WALLET = os.getenv("PAYMENT_WALLET")

# Connect to Ethereum via Infura
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = web3.to_checksum_address(PAYMENT_WALLET)

# Subscription plans
PLANS = {
    "monthly": {"price": 0.01, "duration": 30},   # ETH
    "yearly": {"price": 0.10, "duration": 365},
    "lifetime": {"price": 0.25, "duration": 36500}
}

# Database
DB_PATH = "subscribers.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        plan TEXT,
        expiry TEXT,
        amount REAL,
        tx_hash TEXT
    )""")
    conn.commit()
    conn.close()

def record_subscription(user, plan, tx_hash, amount):
    expiry = datetime.now() + timedelta(days=PLANS[plan]["duration"])
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO subscribers (user, plan, expiry, amount, tx_hash) VALUES (?, ?, ?, ?, ?)",
        (user, plan, expiry.strftime("%Y-%m-%d"), amount, tx_hash)
    )
    conn.commit()
    conn.close()

def check_payment(tx_hash):
    try:
        tx = web3.eth.get_transaction(tx_hash)
        if tx and tx["to"] and tx["to"].lower() == PAYMENT_WALLET.lower():
            return True
    except Exception as e:
        print("❌ Error checking payment:", e)
        return False
    return False

def init_web3():
    return web3, account

if __name__ == "__main__":
    init_db()
    print("✅ Payment Logic initialized and Web3 connected")
