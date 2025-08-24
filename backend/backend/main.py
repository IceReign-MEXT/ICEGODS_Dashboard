# backend/main.py

from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("backend/config/config.env")

# Initialize Flask app
app = Flask(__name__)

# Import payment logic AFTER app creation
from payments import payment_logic

# ---------------------------
# Test home route
# ---------------------------
@app.route("/")
def home():
    return jsonify({"message": "🚀 ICEGODS Dashboard Backend Running!"})

# ---------------------------
# Check wallet balance
# ---------------------------
@app.route("/balance", methods=["GET"])
def get_balance():
    web3, account = payment_logic.init_web3()
    balance = web3.eth.get_balance(account)
    eth_balance = web3.from_wei(balance, 'ether')
    return jsonify({"wallet": account, "balance_eth": str(eth_balance)})

# ---------------------------
# Subscription endpoint
# ---------------------------
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    user = data.get("user")
    plan = data.get("plan")
    tx_hash = data.get("tx_hash")

    if not user or not plan or not tx_hash:
        return jsonify({"error": "Missing required fields"}), 400

    if plan not in payment_logic.PLANS:
        return jsonify({"error": "Invalid plan"}), 400

    if payment_logic.check_payment(tx_hash):
        payment_logic.record_subscription(user, plan, tx_hash, payment_logic.PLANS[plan]["price"])
        return jsonify({"status": "success", "plan": plan}), 200
    else:
        return jsonify({"status": "failed", "reason": "Payment not found"}), 400

# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
