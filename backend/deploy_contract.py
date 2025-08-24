from web3 import Web3
from solcx import compile_standard
import json
import os

# Load .env variables
INFURA_URL = "https://sepolia.infura.io/v3/d91d4edb39b9488897dae682f64b8cbb"
DEPLOYER_PK = "YOUR_PRIVATE_KEY_HERE"
PAYOUT_WALLET = "0x63FC90767faF3c06e7f74a56778b1f805D754F8A"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = w3.eth.account.from_key(DEPLOYER_PK)

# Read Solidity contract
with open("contracts/Subscription.sol", "r") as file:
    contract_source = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"Subscription.sol": {"content": contract_source}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
}, solc_version="0.8.20")

bytecode = compiled_sol['contracts']['Subscription.sol']['Subscription']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['Subscription.sol']['Subscription']['abi']

# Deploy contract
Subscription = w3.eth.contract(abi=abi, bytecode=bytecode)
tx = Subscription.constructor(PAYOUT_WALLET).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 3000000,
    'gasPrice': w3.to_wei('50', 'gwei')
})

signed_tx = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Deploying... tx hash:", tx_hash.hex())

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ Contract deployed at:", receipt.contractAddress)
