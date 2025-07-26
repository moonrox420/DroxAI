import React from 'react';

const Pricing = () => {
  return (
    <div className="bg-gray-100 p-6">
      <h2 className="text-2xl font-bold mb-4">DroxAI Pricing Tiers</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold">Glacier</h3>
          <p>$99/month</p>
          <p>$1,500 onboarding fee</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold">Hollow</h3>
          <p>$299/month</p>
          <p>$5,000 onboarding fee</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold">Forge</h3>
          <p>$599/month</p>
          <p>$15,000 onboarding fee</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold">Brahma</h3>
          <p>$2,999/month</p>
          <p>$25,000 onboarding fee</p>
        </div>
      </div>
      <p className="mt-4">All tiers include unlimited scans with SiteGuardian.</p>
    </div>
  );
};

export default Pricing;
