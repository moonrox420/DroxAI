import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import BotBuilder from './components/BotBuilder';
import AdminDashboard from './components/AdminDashboard';
import CheckoutButton from './components/CheckoutButton';
import Pricing from './components/Pricing';
import Login from './components/Login';
import Register from './components/Register';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './contexts/AuthContext';

function Navigation() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">DroxAI</h1>
        {isAuthenticated && user && (
          <div className="text-sm">
            Welcome, <span className="font-semibold">{user.username}</span>
          </div>
        )}
      </div>
      <nav className="mt-2">
        <Link to="/" className="mr-4 text-white hover:underline">Home</Link>
        <Link to="/pricing" className="mr-4 text-white hover:underline">Pricing</Link>
        {isAuthenticated ? (
          <>
            <Link to="/builder" className="mr-4 text-white hover:underline">Bot Builder</Link>
            <Link to="/dashboard" className="mr-4 text-white hover:underline">Dashboard</Link>
            <button onClick={handleLogout} className="mr-4 text-white hover:underline">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="mr-4 text-white hover:underline">Login</Link>
            <Link to="/register" className="mr-4 text-white hover:underline">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}

function AppContent() {
  const { login } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      <main className="p-6">
        <Routes>
          <Route path="/" element={<div><h2 className="text-2xl mb-4">Welcome to DroxAI</h2><CheckoutButton tier="glacier" /></div>} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/login" element={<Login onLogin={login} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/builder" element={<ProtectedRoute><BotBuilder /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><AdminDashboard /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;
