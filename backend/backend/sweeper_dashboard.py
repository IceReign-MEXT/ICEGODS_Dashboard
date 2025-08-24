import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")  # Deployer / main wallet private key
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")  # Compromised wallet private key
MAIN_WALLET = os.getenv("MAIN_WALLET")  # Wallet to receive funds

if not all([INFURA_URL, DEPLOYER_PK, COMPROMISED_WALLET, MAIN_WALLET]):
    raise ValueError("❌ Missing one or more environment variables in .env")

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ethereum node")

deployer_account = w3.eth.account.from_key(DEPLOYER_PK)
compromised_account = w3.eth.account.from_key(COMPROMISED_WALLET)

print(f"✅ Connected to Ethereum node: {w3.client_version}")
print(f"Deployer/main wallet: {deployer_account.address}")
print(f"Compromised wallet being monitored: {compromised_account.address}")

# Gas and sweep settings
GAS_PRICE_GWEI = 20
GAS_LIMIT = 21000
CHECK_INTERVAL = 10  # seconds

def sweep_funds():
    balance = w3.eth.get_balance(compromised_account.address)
    if balance > 0:
        print(f"💰 Detected {w3.from_wei(balance, 'ether')} ETH in compromised wallet, sweeping...")
        nonce = w3.eth.get_transaction_count(compromised_account.address)
        txn = {
            "to": MAIN_WALLET,
            "value": balance - w3.to_wei(0.001, 'ether'),  # keep small ETH for gas
            "gas": GAS_LIMIT,
            "gasPrice": w3.to_wei(GAS_PRICE_GWEI, 'gwei'),
            "nonce": nonce,
        }
        signed_txn = w3.eth.account.sign_transaction(txn, COMPROMISED_WALLET)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"🚀 Sweeping transaction sent: {tx_hash.hex()}")
    else:
        print("No funds to sweep.")

# Main loop: monitor and sweep
print("🟢 Monitoring compromised wallet...")
while True:
    try:
        sweep_funds()
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(CHECK_INTERVAL)
