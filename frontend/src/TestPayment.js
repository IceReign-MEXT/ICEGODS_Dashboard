import React, { useState } from 'react';

const TestPayment = () => {
  const [status, setStatus] = useState('');

  const handlePayment = async () => {
    setStatus('Processing payment...');

    try {
      const response = await fetch('http://localhost:5000/create-payment-intent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: 1000 }), // amount in cents
      });

      const data = await response.json();

      if (data.client_secret) {
        // Here you would normally use Stripe.js to confirm the payment
        setStatus('Payment intent created. Client secret: ' + data.client_secret);
      } else {
        setStatus('Failed to create payment intent.');
      }
    } catch (error) {
      setStatus('Error: ' + error.message);
    }
  };

  return (
    <div>
      <button onClick={handlePayment} style={{ padding: '10px 20px', cursor: 'pointer' }}>
        Pay $10
      </button>
      <p>{status}</p>
    </div>
  );
};

export default TestPayment;
