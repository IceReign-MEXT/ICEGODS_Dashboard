const hre = require("hardhat");

async function main() {
  const payout = process.env.PAYOUT_WALLET;
  const usdt = process.env.USDT_CONTRACT;
  const price = process.env.SUB_PRICE_USDT || "10000000"; // 10 USDT default (6 decimals)

  if (!payout || !usdt) throw new Error("env missing");

  const Pay = await hre.ethers.getContractFactory("USDTPayments");
  const pay = await Pay.deploy(usdt, payout, price);
  await pay.deployed();
  console.log("USDTPayments deployed at:", pay.address);
}

main().catch((e) => { console.error(e); process.exit(1); });
