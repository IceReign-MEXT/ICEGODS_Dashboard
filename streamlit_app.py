import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICEGODS Dashboard", layout="wide")

st.title("🛡️ ICEGODS Blockchain Defense Dashboard")
st.write("Monitoring wallets, detecting threats, and managing defense bots in real time.")

# Example wallet table
wallets = pd.DataFrame({
    "Wallet": ["0x1234...abcd", "0xabcd...9876"],
    "Balance": ["2.5 ETH", "13.2 MATIC"],
    "Threat Level": ["Low", "High"]
})
st.subheader("📊 Wallet Monitoring")
st.dataframe(wallets)

# Example bot status
st.subheader("🤖 Defense Bots")
st.success("MasterBot: Running")
st.warning("WolfGuard: Needs Attention")
st.info("PhoenixReign: Idle")
