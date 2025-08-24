#!/usr/bin/env python3
import os
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
INFURA_SECRET = os.getenv("INFURA_SECRET", "")
w3 = Web3(Web3.HTTPProvider(INFURA_URL, request_kwargs={"auth": ("", INFURA_SECRET)}) if INFURA_SECRET else Web3.HTTPProvider(INFURA_URL))

USDT_ADDRESS = Web3.to_checksum_address(os.getenv("USDT_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7"))
USDT_ABI = [
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"}
]

compromised_pk = os.getenv("COMPROMISED_PK")   # 0x...
to_addr = Web3.to_checksum_address(os.getenv("SAFE_ADDR"))
usdt = w3.eth.contract(address=USDT_ADDRESS, abi=USDT_ABI)

acct = w3.eth.account.from_key(compromised_pk)
balance = usdt.functions.balanceOf(acct.address).call()
decimals = usdt.functions.decimals().call()
print("USDT balance (raw):", balance, " => human:", balance / (10**decimals))

# choose amount to transfer (in human units)
amount_human = float(input("Amount of USDT to transfer (human): "))
amount_raw = int(amount_human * (10**decimals))

# Build transaction
nonce = w3.eth.get_transaction_count(acct.address)
tx = usdt.functions.transfer(to_addr, amount_raw).build_transaction({
    "chainId": 1,
    "gas": 150000,
    "gasPrice": w3.eth.gas_price,
    "nonce": nonce,
    "from": acct.address
})

print("Estimated gas price (wei):", w3.eth.gas_price)
print("Signing transaction...")

signed = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Sent TX:", tx_hash.hex())
print("Check Etherscan: https://etherscan.io/tx/" + tx_hash.hex())
