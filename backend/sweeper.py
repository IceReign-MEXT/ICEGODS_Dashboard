import os, math
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
RPC = os.getenv("INFURA_URL") or os.getenv("ALCHEMY_URL")
PK  = (os.getenv("DEPLOYER_PK") or "").strip().replace("0x","")
SRC = os.getenv("COMPROMISED_WALLET")
DST = os.getenv("MAIN_WALLET")

if not (RPC and PK and SRC and DST):
    raise SystemExit("Missing .env: INFURA_URL/ALCHEMY_URL, DEPLOYER_PK, COMPROMISED_WALLET, MAIN_WALLET")

w3 = Web3(Web3.HTTPProvider(RPC))
acct = w3.eth.account.from_key(PK)
assert acct.address.lower() == SRC.lower(), "DEPLOYER_PK does not match COMPROMISED_WALLET"

USDT = w3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7")
USDT_ABI = [
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
     "name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],
     "name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
]
usdt = w3.eth.contract(address=USDT, abi=USDT_ABI)
DST = w3.to_checksum_address(DST)

def eip1559_fees():
    base = w3.eth.gas_price  # fallback if base_fee not exposed
    try:
        block = w3.eth.get_block("latest")
        base = block.get("baseFeePerGas", base)
    except: pass
    max_priority = w3.to_wei("1.5", "gwei")
    max_fee = int(base + max_priority*2)
    return max_priority, max_fee

def sweep_eth():
    bal = w3.eth.get_balance(acct.address)
    if bal <= 0: 
        print("No ETH to sweep"); return
    max_prio, max_fee = eip1559_fees()
    est_gas = 21000
    cost = est_gas * max_fee
    send_value = bal - cost
    if send_value <= 0:
        print("Not enough ETH for gas"); return
    tx = {
        "to": DST,
        "value": send_value,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "chainId": 1,
        "type": 2,
        "maxPriorityFeePerGas": max_prio,
        "maxFeePerGas": max_fee,
        "gas": est_gas,
    }
    signed = w3.eth.account.sign_transaction(tx, PK)
    h = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("✅ ETH swept tx:", h.hex())

def sweep_usdt():
    bal = usdt.functions.balanceOf(acct.address).call()
    if bal <= 0:
        print("No USDT to sweep"); return
    max_prio, max_fee = eip1559_fees()
    nonce = w3.eth.get_transaction_count(acct.address)
    tx = usdt.functions.transfer(DST, bal).build_transaction({
        "from": acct.address,
        "chainId": 1,
        "nonce": nonce,
        "type": 2,
        "maxPriorityFeePerGas": max_prio,
        "maxFeePerGas": max_fee,
        "gas": 100000,
    })
    signed = w3.eth.account.sign_transaction(tx, PK)
    h = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("✅ USDT swept tx:", h.hex())

if __name__ == "__main__":
    print("🚨 Sweeper running")
    sweep_eth()
    sweep_usdt()
    print("Done.")
