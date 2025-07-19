import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import BotBuilder from './components/BotBuilder';
import AdminDashboard from './components/AdminDashboard';
import CheckoutButton from './components/CheckoutButton';
import Pricing from './components/Pricing';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-blue-600 text-white p-4">
          <h1 className="text-3xl font-bold">DroxAI</h1>
          <nav className="mt-2">
            <Link to="/" className="mr-4 text-white hover:underline">Home</Link>
            <Link to="/pricing" className="mr-4 text-white hover:underline">Pricing</Link>
            <Link to="/builder" className="mr-4 text-white hover:underline">Bot Builder</Link>
            <Link to="/dashboard" className="mr-4 text-white hover:underline">Admin Dashboard</Link>
          </nav>
        </header>
        <main className="p-6">
          <Routes>
            <Route path="/" element={<div><h2 className="text-2xl mb-4">Welcome to DroxAI</h2><CheckoutButton tier="glacier" /></div>} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/builder" element={<BotBuilder />} />
            <Route path="/dashboard" element={<AdminDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
