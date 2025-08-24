from eth_account import Account
from mnemonic import Mnemonic
from dotenv import load_dotenv
import os, csv, sys

DERIVATION_PREFIX = "m/44'/60'/0'/0/"  # Ethereum standard

def load_seed_from_env():
    load_dotenv()
    seed = os.getenv("SEED_PHRASE", "").strip().strip('"').strip("'")
    if not seed:
        sys.exit("❌ SEED_PHRASE missing in .env")
    words = seed.split()
    if len(words) not in (12, 24):
        sys.exit("❌ SEED_PHRASE must be 12 or 24 words")
    return seed

def derive_many(seed_phrase, count):
    rows = []
    for i in range(count):
        path = f"{DERIVATION_PREFIX}{i}"
        acct = Account.from_mnemonic(seed_phrase, account_path=path)
        rows.append({
            "index": i,
            "path": path,
            "address": acct.address,
            "private_key": acct._private_key.hex()  # includes 0x
        })
    return rows

def write_csv(rows, out_path):
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["index","path","address","private_key"])
        w.writeheader()
        w.writerows(rows)

def update_env(address, private_key_hex, env_path=".env"):
    pk_no0x = private_key_hex.replace("0x","")
    # Read existing lines except our keys
    lines = []
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                key = line.split("=",1)[0].strip() if "=" in line and not line.strip().startswith("#") else None
                if key in ("COMPROMISED_WALLET","DEPLOYER_PK"):
                    continue
                lines.append(line.rstrip("\n"))
    # Append our values
    lines.append(f"COMPROMISED_WALLET={address}")
    lines.append(f"DEPLOYER_PK={pk_no0x}")
    with open(env_path, "w") as f:
        for line in lines:
            f.write(line + ("\n" if not line.endswith("\n") else ""))
    print(f"✅ Wrote COMPROMISED_WALLET and DEPLOYER_PK to {env_path}")

def main():
    # How many?
    try:
        count = int((input("How many addresses to derive? [10]: ") or "10").strip())
    except:
        count = 10

    seed = load_seed_from_env()
    rows = derive_many(seed, count)

    print("\nDerived Ethereum addresses:")
    for r in rows:
        print(f"[{r['index']:02d}] {r['address']}  ({r['path']})")

    show = input("\nShow private keys now? (y/N): ").strip().lower()
    if show == "y":
        for r in rows:
            print(f"[{r['index']:02d}] {r['address']}  PK={r['private_key']}")

    out_csv = "derived_eth_addresses.csv"
    write_csv(rows, out_csv)
    print(f"\n📄 Saved {out_csv}. Keep it SECRET and offline.")

    pick = input("\nPick index to export to .env as COMPROMISED_WALLET/DEPLOYER_PK (blank to skip): ").strip()
    if pick != "":
        i = int(pick)
        if i < 0 or i >= len(rows):
            sys.exit("Invalid index.")
        update_env(rows[i]["address"], rows[i]["private_key"])
        print("⚠️ Make sure .env also has INFURA_URL (or ALCHEMY_URL) and MAIN_WALLET set.")

    print("\nDone.")

if __name__ == "__main__":
    main()
