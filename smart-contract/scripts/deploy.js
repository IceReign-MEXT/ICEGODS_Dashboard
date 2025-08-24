const hre = require("hardhat");

async function main() {
  const payout = process.env.PAYOUT_WALLET;
  if (!payout) throw new Error("PAYOUT_WALLET missing in .env");

  const Factory = await hre.ethers.getContractFactory("SubscriptionManager");
  const contract = await Factory.deploy(payout);
  await contract.deployed();

  console.log("SubscriptionManager deployed at:", contract.address);
  console.log("Payout wallet:", payout);
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
