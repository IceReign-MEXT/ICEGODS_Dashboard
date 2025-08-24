import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
RPC = os.getenv("DEPLOY_RPC")
PK  = os.getenv("DEPLOYER_PK")  # compromised wallet PK (no 0x)
TO  = Web3.to_checksum_address(os.getenv("PAYOUT_WALLET"))
USDT = Web3.to_checksum_address(os.getenv("USDT_CONTRACT", "0xdAC17F958D2ee523a2206206994597C13D831ec7"))

w3 = Web3(Web3.HTTPProvider(RPC))
acct = w3.eth.account.from_key(PK)

usdt_abi = [{"constant":True,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},
            {"constant":False,"inputs":[{"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
            {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]
token = w3.eth.contract(address=USDT, abi=usdt_abi)

bal = token.functions.balanceOf(acct.address).call()
dec = token.functions.decimals().call()
print(f"USDT balance: {bal/(10**dec)}")

if bal == 0:
    print("Nothing to sweep.")
    raise SystemExit

tx = token.functions.transfer(TO, bal).build_transaction({
    "from": acct.address,
    "nonce": w3.eth.get_transaction_count(acct.address),
    "gas": 100000,
    "maxFeePerGas": w3.to_wei("20", "gwei"),
    "maxPriorityFeePerGas": w3.to_wei("1.5", "gwei"),
    "chainId": w3.eth.chain_id
})
signed = w3.eth.account.sign_transaction(tx, PK)
txh = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Sweep tx:", txh.hex())
