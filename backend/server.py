#!/usr/bin/env python3.6
# Python 3.6+ required

import os
import json
from flask import Flask, request, jsonify
import stripe
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Simple test route
@app.route('/')
def home():
    return jsonify({"message": "🚀 ICEGODS Dashboard Backend Running!"})

# Stripe webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        else:
            event = json.loads(payload)
    except ValueError as e:
        print("⚠️  Invalid payload:", e)
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        print("⚠️  Webhook signature verification failed:", e)
        return jsonify(success=False), 400

    # Handle events
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(f"✅ Payment succeeded for {payment_intent['amount']}")
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']
        print(f"💳 Payment method attached: {payment_method['id']}")
        # handle_payment_method_attached(payment_method)
    else:
        print(f"ℹ️ Unhandled event type {event['type']}")

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
