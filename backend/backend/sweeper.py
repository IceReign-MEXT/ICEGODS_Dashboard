import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
DEPLOYER_PK = os.getenv("DEPLOYER_PK")
COMPROMISED_WALLET = os.getenv("COMPROMISED_WALLET")
MAIN_WALLET = os.getenv("MAIN_WALLET")

if not INFURA_URL or not DEPLOYER_PK or not COMPROMISED_WALLET or not MAIN_WALLET:
    raise ValueError("❌ Missing .env: INFURA_URL, DEPLOYER_PK, COMPROMISED_WALLET, MAIN_WALLET")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise ConnectionError("❌ Unable to connect to Ethereum node")

acct = w3.eth.account.from_key(DEPLOYER_PK)
assert acct.address.lower() == COMPROMISED_WALLET.lower(), "DEPLOYER_PK does not match COMPROMISED_WALLET"

balance = w3.eth.get_balance(COMPROMISED_WALLET)
print(f"💰 Compromised wallet balance: {w3.from_wei(balance, 'ether')} ETH")

if balance > 0:
    tx = {
        "from": COMPROMISED_WALLET,
        "to": MAIN_WALLET,
        "value": balance - w3.to_wei("0.001", "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "nonce": w3.eth.get_transaction_count(COMPROMISED_WALLET),
    }
    signed_tx = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"🚀 Sweeping funds... tx hash: {tx_hash.hex()}")
else:
    print("⚠️ No funds to sweep")
