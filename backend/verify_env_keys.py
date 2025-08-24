import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
pk = (os.getenv("DEPLOYER_PK") or "").strip().replace("0x","")
src = (os.getenv("COMPROMISED_WALLET") or "").strip()
if not pk or not src:
    raise SystemExit("Missing DEPLOYER_PK or COMPROMISED_WALLET in .env")
acct = Web3().eth.account.from_key(pk)
print("Derived from PK:", acct.address)
print("Env COMPROMISED:", src)
print("MATCH:", acct.address.lower() == src.lower())
