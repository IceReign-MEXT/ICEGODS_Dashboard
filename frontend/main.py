from flask import Flask, request, jsonify
from payments import payment_logic

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "🚀 ICEGODS Dashboard Backend Running!"})

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    user = data.get("user")
    plan = data.get("plan")
    tx_hash = data.get("tx_hash")

    if not user or not plan or not tx_hash:
        return jsonify({"status": "fail", "reason": "Missing fields"}), 400

    success = payment_logic.verify_payment(tx_hash, plan)

    if success:
        # You can add DB recording here
        return jsonify({"status": "success", "user": user, "plan": plan}), 200
    else:
        return jsonify({"status": "fail", "reason": "Payment not found"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
