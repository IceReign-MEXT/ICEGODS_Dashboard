import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
RPC = os.getenv("INFURA_URL") or os.getenv("ALCHEMY_URL")
WALLET = os.getenv("COMPROMISED_WALLET")
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

if not RPC or not WALLET:
    raise SystemExit("Set INFURA_URL/ALCHEMY_URL and COMPROMISED_WALLET in .env")

w3 = Web3(Web3.HTTPProvider(RPC))
print("RPC connected:", w3.is_connected())
addr = Web3.to_checksum_address(WALLET)

# ETH
eth = w3.from_wei(w3.eth.get_balance(addr), "ether")
print(f"ETH balance: {eth} ETH")

# USDT (6 decimals)
usdt = w3.eth.contract(address=Web3.to_checksum_address(USDT), abi=[
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],
     "name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}
])
raw = usdt.functions.balanceOf(addr).call()
print(f"USDT balance: {raw/1_000_000:.6f} USDT")
