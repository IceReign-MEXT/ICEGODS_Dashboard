from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET")
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")

w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))

balance = w3.eth.get_balance(COMPROMISED_WALLET)
print(f"Balance of {COMPROMISED_WALLET}: {w3.from_wei(balance, 'ether')} ETH")
