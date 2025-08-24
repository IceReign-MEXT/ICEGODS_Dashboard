from web3 import Web3
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET")

# Connect to Infura using HTTP provider with secret
w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))

# Test connection
print("Connected:", w3.is_connected())
