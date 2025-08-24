const hre = require("hardhat");

async function main() {
  const payout = process.env.PAYOUT_WALLET;
  if (!payout) throw new Error("PAYOUT_WALLET missing");

  const Fwd = await hre.ethers.getContractFactory("ETHForwarder");
  const fwd = await Fwd.deploy(payout);
  await fwd.deployed();
  console.log("ETHForwarder deployed at:", fwd.address);
}

main().catch((e) => { console.error(e); process.exit(1); });
