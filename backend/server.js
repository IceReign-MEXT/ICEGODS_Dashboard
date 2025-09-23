import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import Stripe from 'stripe';

dotenv.config();

const app = express();
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

app.use(cors());
app.use(express.json());

// Test route
app.get('/', (req, res) => {
  res.send('🚀 ICEGODS Backend Running!');
});

// --- Stripe Checkout session ---
app.post('/create-checkout-session', async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'subscription',
      line_items: [
        {
          price: 'price_1YourStripePriceID', // Replace with your Stripe price ID
          quantity: 1,
        },
      ],
      success_url: `${process.env.FRONTEND_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.FRONTEND_URL}/cancel`,
    });

    res.json({ id: session.id });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Stripe session failed' });
  }
});

// --- Start server ---
const PORT = process.env.PORT || 5003;
app.listen(PORT, () => console.log(`🚀 Backend running on http://localhost:${PORT}`));
