#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import stripe
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Stripe keys from .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get("amount")

        if not amount:
            return jsonify({"error": "Amount is required"}), 400

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
        )

        return jsonify({"client_secret": intent.client_secret})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
