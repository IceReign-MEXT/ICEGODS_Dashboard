from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv
import time
import requests

# Load .env variables
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")
MAIN_WALLET = os.getenv("MAIN_WALLET")
SUB_PRICE = float(os.getenv("SUB_PRICE", "0.01"))  # ETH
TG_BOT = os.getenv("TG_BOT")                        # Telegram bot token
TG_CHAT_ID = os.getenv("TG_CHAT_ID")                # Telegram chat ID

# ERC-20 token contract address (example USDT)
USDT_ADDRESS = Web3.to_checksum_address(os.getenv("USDT_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7"))
USDT_ABI = [
    {
        "constant":True,"inputs":[{"name":"_owner","type":"address"}],
        "name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],
        "type":"function"
    },
    {
        "constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
        "name":"transfer","outputs":[{"name":"success","type":"bool"}],
        "type":"function"
    }
]

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if not w3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ethereum node.")

print("✅ Connected to Ethereum node")
acct = w3.eth.account.from_key(DEPLOYER_PK)
print("Deployer:", acct.address)
print("Compromised wallet:", COMPROMISED_WALLET)
print(f"Subscription price: {SUB_PRICE} ETH")
print("🔄 Starting wallet monitor...")

# USDT contract
usdt_contract = w3.eth.contract(address=USDT_ADDRESS, abi=USDT_ABI)

def send_telegram(message):
    if TG_BOT and TG_CHAT_ID:
        url = f"https://api.telegram.org/bot{TG_BOT}/sendMessage"
        data = {"chat_id": TG_CHAT_ID, "text": message}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print("⚠️ Telegram send error:", e)

def sweep_eth():
    balance = w3.eth.get_balance(COMPROMISED_WALLET)
    if balance > 0:
        gas_price = w3.eth.gas_price
        gas_estimate = 21000
        total_gas_cost = gas_price * gas_estimate
        amount_to_send = balance - total_gas_cost
        if amount_to_send > 0:
            tx = {
                'to': MAIN_WALLET,
                'value': amount_to_send,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'nonce': w3.eth.get_transaction_count(acct.address),
                'chainId': 1
            }
            signed_tx = acct.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"💸 Swept {w3.from_wei(amount_to_send,'ether')} ETH to main wallet")
            send_telegram(f"💸 Swept {w3.from_wei(amount_to_send,'ether')} ETH to main wallet\nTx: {tx_hash.hex()}")

def sweep_usdt():
    balance = usdt_contract.functions.balanceOf(COMPROMISED_WALLET).call()
    if balance > 0:
        nonce = w3.eth.get_transaction_count(acct.address)
        tx = usdt_contract.functions.transfer(MAIN_WALLET, balance).build_transaction({
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': 1
        })
        signed_tx = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"💸 Swept {balance/1e6} USDT to main wallet")
        send_telegram(f"💸 Swept {balance/1e6} USDT to main wallet\nTx: {tx_hash.hex()}")

while True:
    try:
        sweep_eth()
        sweep_usdt()
        time.sleep(15)  # check every 15 seconds
    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(15)
