import dotenv from 'dotenv';
dotenv.config();

import fetch from 'node-fetch';

// 1️⃣ Check environment variables
console.log("Checking backend environment variables...");
console.log("PORT:", process.env.PORT);
console.log("STRIPE_PUBLISHABLE_KEY:", process.env.STRIPE_PUBLISHABLE_KEY ? "✅ Loaded" : "❌ Missing");
console.log("STRIPE_SECRET_KEY:", process.env.STRIPE_SECRET_KEY ? "✅ Loaded" : "❌ Missing");
console.log("BACKEND URL:", process.env.FRONTEND_URL);

// 2️⃣ Check bots endpoint
const backendURL = `http://localhost:${process.env.PORT || 5003}`;

fetch(`${backendURL}/bots`)
  .then(res => res.json())
  .then(data => {
    console.log("Bots endpoint working. Sample data:", data.slice(0, 3));
  })
  .catch(err => console.error("Bots endpoint failed:", err));

// 3️⃣ Check Stripe key format
if (process.env.STRIPE_PUBLISHABLE_KEY?.startsWith("pk_") &&
    process.env.STRIPE_SECRET_KEY?.startsWith("sk_")) {
  console.log("Stripe keys format looks correct ✅");
} else {
  console.log("Stripe keys format looks wrong ❌");
}
