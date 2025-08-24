require("@nomicfoundation/hardhat-toolbox");

const RPC = process.env.DEPLOY_RPC || "https://sepolia.infura.io/v3/YOUR_KEY";
const PK  = process.env.DEPLOYER_PK ? [process.env.DEPLOYER_PK] : [];

module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: { url: RPC, accounts: PK },
    mainnet: { url: RPC, accounts: PK }
  }
};
