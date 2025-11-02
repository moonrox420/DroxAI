import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const AdminDashboard = () => {
  const { user } = useAuth();

  return (
    <div className="bg-gray-100 p-6">
      <h2 className="text-2xl font-bold mb-4">Admin Dashboard</h2>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-2">User Information</h3>
        <p><strong>Username:</strong> {user?.username}</p>
        <p><strong>Email:</strong> {user?.email}</p>
        <p><strong>Account Created:</strong> {new Date(user?.created_at).toLocaleDateString()}</p>
      </div>
      <div className="mt-6 bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-2">System Status</h3>
        <p className="text-green-600">All systems operational</p>
      </div>
    </div>
  );
};

export default AdminDashboard;
