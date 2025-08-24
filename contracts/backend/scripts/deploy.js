const hre = require("hardhat");

async function main() {
  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  // Compile & deploy Subscription contract
  const Subscription = await hre.ethers.getContractFactory("Subscription");
  const contract = await Subscription.deploy(
    process.env.PAYOUT_WALLET // payout wallet from .env
  );

  await contract.deployed();
  console.log("Subscription contract deployed to:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
