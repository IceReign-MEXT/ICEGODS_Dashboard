import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv('../config/config.env')  # Load your .env

# Load environment variables
INFURA_URL = os.getenv("INFURA_URL")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")
PAYOUT_WALLET = os.getenv("PAYOUT_WALLET")
SUBSCRIPTION_CONTRACT = os.getenv("SUBSCRIPTION_CONTRACT")

# Connect to Web3
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if w3.isConnected():
    print("✅ Payment Logic initialized and Web3 connected")
else:
    print("❌ Web3 connection failed")

# Load subscription contract
subscription_abi = [
    {
        "inputs":[{"internalType":"address","name":"_payoutWallet","type":"address"}],
        "stateMutability":"nonpayable",
        "type":"constructor"
    },
    {
        "inputs":[{"internalType":"address","name":"_user","type":"address"}],
        "name":"getSubscription",
        "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
        "stateMutability":"view",
        "type":"function"
    },
    {
        "inputs":[],
        "name":"subscribe",
        "outputs":[],
        "stateMutability":"payable",
        "type":"function"
    }
]

if not SUBSCRIPTION_CONTRACT:
    print("⚠️ SUBSCRIPTION_CONTRACT not set in .env")
else:
    contract = w3.eth.contract(address=SUBSCRIPTION_CONTRACT, abi=subscription_abi)

# Function to create subscription transaction
def create_subscription_transaction(subscriber_address):
    tx = contract.functions.subscribe().buildTransaction({
        'from': subscriber_address,
        'value': w3.toWei(0.01, 'ether'),
        'gas': 200000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': w3.eth.getTransactionCount(subscriber_address)
    })
    return tx

# Function to send ETH (simulate subscription)
def send_subscription(subscriber_address, private_key):
    tx = create_subscription_transaction(subscriber_address)
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"✅ Subscription sent: {w3.toHex(tx_hash)}")
    return w3.toHex(tx_hash)
