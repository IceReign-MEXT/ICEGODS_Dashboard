from web3 import Web3

# Replace with your Infura URL
INFURA_URL = "https://mainnet.infura.io/v3/eccc3a80363543be80d7d603b9533f01"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

print("Connected:", w3.is_connected())
