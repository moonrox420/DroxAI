import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { REQUIRE_AUTH } from '../config';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // If authentication is disabled, allow access
  if (!REQUIRE_AUTH) {
    return children;
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
