import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
WALLET = os.getenv("MAIN_WALLET")

if not INFURA_URL or not WALLET:
    raise ValueError("Please set INFURA_URL and MAIN_WALLET in .env")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ethereum node")

balance = w3.eth.get_balance(WALLET)
print(f"💰 Wallet {WALLET} balance: {w3.from_wei(balance, 'ether')} ETH")
