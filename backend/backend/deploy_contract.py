import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
INFURA_URL = os.getenv("INFURA_URL")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")
PAYOUT_WALLET = os.getenv("PAYOUT_WALLET")

# Validate deployer key
if not DEPLOYER_PK or len(DEPLOYER_PK) != 64:
    raise ValueError("❌ DEPLOYER_PK is invalid. It should be a 64-character hex string without 0x prefix.")

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = w3.eth.account.from_key(DEPLOYER_PK)
print(f"✅ Connected to {w3.clientVersion}")
print(f"Deployer: {account.address}")

# Install Solidity compiler
install_solc("0.8.20")

# Read smart contract source
with open("backend/contracts/Subscription.sol", "r") as file:
    subscription_source = file.read()

# Compile the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Subscription.sol": {"content": subscription_source}},
        "settings": {
            "outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}
        },
    },
    solc_version="0.8.20",
)

# Extract ABI and bytecode
abi = compiled_sol["contracts"]["Subscription.sol"]["Subscription"]["abi"]
bytecode = compiled_sol["contracts"]["Subscription.sol"]["Subscription"]["evm"]["bytecode"]["object"]

# Create contract instance
Subscription = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build deployment transaction
construct_txn = Subscription.constructor(PAYOUT_WALLET).build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
})

# Sign and send transaction
signed = account.sign_transaction(construct_txn)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print(f"🚀 Deploying contract... tx hash: {tx_hash.hex()}")

# Wait for transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")

# Save ABI and address
with open("backend/contracts/Subscription.json", "w") as f:
    json.dump({"abi": abi, "address": tx_receipt.contractAddress}, f)

print("📂 ABI and contract address saved to backend/contracts/Subscription.json")
