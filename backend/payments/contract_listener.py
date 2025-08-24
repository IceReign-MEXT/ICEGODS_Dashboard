import os
import json
import sqlite3
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv("backend/config/config.env")

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("SUBSCRIPTION_CONTRACT")  # set after deploy

ABI = [
  {
    "anonymous": False,
    "inputs": [
      {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
      {"indexed": True, "internalType": "uint8", "name": "plan", "type": "uint8"},
      {"indexed": False, "internalType": "uint256", "name": "amountWei", "type": "uint256"},
      {"indexed": False, "internalType": "uint256", "name": "newExpiry", "type": "uint256"}
    ],
    "name": "Subscribed",
    "type": "event"
  }
]

DB_PATH = "subscribers.db"

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS subscribers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user TEXT,
      plan TEXT,
      expiry TEXT,
      amountWei TEXT,
      tx_hash TEXT
    )""")
    conn.commit()
    conn.close()

def main():
    ensure_db()
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

    print("➡️  Listening for Subscribed events...")
    from_block = "latest"
    while True:
        try:
            events = contract.events.Subscribed.get_logs(fromBlock=from_block)
            for ev in events:
                args = ev["args"]
                user = args["user"]
                plan = str(args["plan"])
                expiry_ts = int(args["newExpiry"])
                amount_wei = str(args["amountWei"])
                tx_hash = ev["transactionHash"].hex()
                expiry_date = datetime.utcfromtimestamp(expiry_ts).strftime("%Y-%m-%d")

                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO subscribers (user, plan, expiry, amountWei, tx_hash) VALUES (?, ?, ?, ?, ?)",
                    (user, plan, expiry_date, amount_wei, tx_hash)
                )
                conn.commit()
                conn.close()
                print(f"✅ Recorded {user} plan={plan} exp={expiry_date} tx={tx_hash}")
            from_block = "latest"
        except Exception as e:
            # Polling fallback
            pass

if __name__ == "__main__":
    if not CONTRACT_ADDRESS:
        raise SystemExit("Set SUBSCRIPTION_CONTRACT in backend/config/config.env")
    main()
