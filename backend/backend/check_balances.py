import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Load env variables
INFURA_URL = os.getenv("INFURA_URL")
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")
MAIN_WALLET = os.getenv("MAIN_WALLET")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    print("❌ Not connected to Ethereum node")
    exit()

def eth_balance(address):
    balance = w3.eth.get_balance(address)
    return w3.from_wei(balance, "ether")

print("✅ Connected to Ethereum")
print(f"Compromised Wallet ({COMPROMISED_WALLET}) Balance: {eth_balance(COMPROMISED_WALLET)} ETH")
print(f"Main Wallet ({MAIN_WALLET}) Balance: {eth_balance(MAIN_WALLET)} ETH")
