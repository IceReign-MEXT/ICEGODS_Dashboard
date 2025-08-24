# check_connection.py
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Print connection status
print("Connected:", w3.is_connected())
