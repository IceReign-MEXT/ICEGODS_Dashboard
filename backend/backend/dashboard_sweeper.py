# nano backend/dashboard_sweeper.py

from web3 import Web3
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")  # Your main wallet private key
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")  # Private key of monitored wallet
MAIN_WALLET = os.getenv("MAIN_WALLET")  # Where funds are swept

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))

if not w3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ethereum node")

# Prepare accounts
deployer = w3.eth.account.from_key(DEPLOYER_PK)
compromised = w3.eth.account.from_key(COMPROMISED_WALLET)

print("✅ Connected to Ethereum node")
print(f"Deployer: {deployer.address}")
print(f"Compromised wallet: {compromised.address}")

# Function to sweep ETH
def sweep_eth():
    balance = w3.eth.get_balance(compromised.address)
    if balance > 0:
        txn = {
            'to': MAIN_WALLET,
            'value': balance - w3.to_wei(0.001, 'ether'),  # leave tiny gas buffer
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(compromised.address),
        }
        signed_txn = compromised.sign_transaction(txn)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"💸 Swept {w3.from_wei(balance, 'ether')} ETH → {MAIN_WALLET} | Tx: {tx_hash.hex()}")
    else:
        print("ℹ️ No ETH to sweep right now")

# Loop to monitor continuously
while True:
    try:
        sweep_eth()
        # You can add ERC-20 token sweeping here later
    except Exception as e:
        print("⚠️ Error:", e)
    time.sleep(15)  # Check every 15 seconds
