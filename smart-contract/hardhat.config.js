require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

const INFURA_PROJECT_ID = process.env.INFURA_PROJECT_ID;
const PRIVATE_KEY = process.env.DEPLOYER_PK; // never commit this

module.exports = {
  solidity: "0.8.24",
  networks: {
    sepolia: {
      url: `https://sepolia.infura.io/v3/${INFURA_PROJECT_ID}`,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : []
    },
    mainnet: {
      url: `https://mainnet.infura.io/v3/${INFURA_PROJECT_ID}`,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : []
    }
  }
};
