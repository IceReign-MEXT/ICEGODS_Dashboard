from eth_account import Account
from mnemonic import Mnemonic
from getpass import getpass
import os, csv
from dotenv import dotenv_values

DERIVATION_PREFIX = "m/44'/60'/0'/0/"  # Ethereum standard

def load_seed():
    print("⚠️ Your seed phrase is only used locally and never leaves this device.")
    seed = getpass("Enter your 12/24-word seed phrase: ").strip()
    if len(seed.split()) not in (12, 24):
        raise SystemExit("Seed phrase must be 12 or 24 words.")
    return seed

def derive_many(seed_phrase, count):
    rows = []
    for i in range(count):
        path = f"{DERIVATION_PREFIX}{i}"
        acct = Account.from_mnemonic(seed_phrase, account_path=path)
        rows.append({"index": i, "path": path, "address": acct.address, "private_key": acct._private_key.hex()})
    return rows

def write_csv(rows, out_path):
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["index", "path", "address", "private_key"])
        w.writeheader()
        w.writerows(rows)

def update_env(env_path, compromised_addr, private_key_no0x):
    # load existing .env
    lines = []
    seen = set()
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                key = line.split("=", 1)[0].strip() if "=" in line and not line.strip().startswith("#") else None
                if key in ("COMPROMISED_WALLET", "DEPLOYER_PK"):
                    continue
                lines.append(line.rstrip("\n"))

    lines.append(f"COMPROMISED_WALLET={compromised_addr}")
    lines.append(f"DEPLOYER_PK={private_key_no0x}")  # no 0x
    with open(env_path, "w") as f:
        for line in lines:
            f.write(line + ("\n" if not line.endswith("\n") else ""))
    print(f"✅ Updated {env_path} with COMPROMISED_WALLET and DEPLOYER_PK")

def main():
    try:
        count_raw = input("How many addresses to derive? [10]: ").strip() or "10"
        count = int(count_raw)
    except:
        count = 10

    seed = load_seed()
    rows = derive_many(seed, count)

    # Print addresses (safe)
    print("\nDerived Ethereum addresses:")
    for r in rows:
        print(f"[{r['index']:02d}] {r['address']}  ({r['path']})")

    # Optional: show private keys
    show = input("\nShow private keys now? (y/N): ").strip().lower()
    if show == "y":
        for r in rows:
            print(f"[{r['index']:02d}] {r['address']}  PK={r['private_key']}")

    # Save CSV for your records
    out_csv = "derived_eth_addresses.csv"
    write_csv(rows, out_csv)
    print(f"\n📄 Saved {out_csv} (index,address,private_key). Keep it SECRET.")

    # Optionally export one to .env
    pick = input("\nPick index to export to .env as COMPROMISED_WALLET/DEPLOYER_PK (blank to skip): ").strip()
    if pick != "":
        i = int(pick)
        if i < 0 or i >= len(rows):
            raise SystemExit("Invalid index.")
        addr = rows[i]["address"]
        pk_no0x = rows[i]["private_key"].replace("0x", "")
        update_env(".env", addr, pk_no0x)
        print("⚠️ Verify your .env also has INFURA_URL and MAIN_WALLET set.")

    print("\nDone.")

if __name__ == "__main__":
    main()
