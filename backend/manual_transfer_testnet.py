#!/usr/bin/env python3
# manual_transfer_testnet.py — build, sign, broadcast a token transfer on testnet
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
load_dotenv(".env.test")

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # private key of the wallet that holds the tokens (0x...)
SAFE_ADDR = os.getenv("SAFE_ADDRESS")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")

if INFURA_SECRET:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}))
else:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise SystemExit("❌ RPC connection failed")

acct = Account.from_key(PRIVATE_KEY)
print("Using account:", acct.address)

ERC20_ABI = [
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"}
]
token = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=ERC20_ABI)
decimals = token.functions.decimals().call()
raw_balance = token.functions.balanceOf(acct.address).call()
print("Token balance:", raw_balance / (10**decimals))

amount = float(input("Amount to send (human units, e.g. 10.5): ").strip())
raw_amount = int(amount * (10**decimals))

nonce = w3.eth.get_transaction_count(acct.address)
# build tx
txn = token.functions.transfer(Web3.to_checksum_address(SAFE_ADDR), raw_amount).build_transaction({
    "chainId": w3.eth.chain_id,
    "gas": 200000,
    "gasPrice": w3.eth.gas_price,
    "nonce": nonce,
    "from": acct.address
})

signed = acct.sign_transaction(txn)
txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Transaction sent. TX hash:", txhash.hex())
print("Check explorer (Sepolia): https://sepolia.etherscan.io/tx/" + txhash.hex())
