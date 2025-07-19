import React from 'react';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe('YOUR_STRIPE_PUBLISHABLE_KEY');

const CheckoutButton = ({ tier }) => {
  const handleCheckout = async () => {
    const stripe = await stripePromise;
    try {
      const response = await fetch('https://api.droxai.com/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tier })
      });
      const session = await response.json();
      await stripe.redirectToCheckout({ sessionId: session.id });
    } catch (error) {
      console.error('Checkout failed:', error);
      alert('Failed to initiate checkout. Please try again.');
    }
  };

  return (
    <button
      className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      onClick={handleCheckout}
    >
      Buy {tier.charAt(0).toUpperCase() + tier.slice(1)} Plan
    </button>
  );
};

export default CheckoutButton;
