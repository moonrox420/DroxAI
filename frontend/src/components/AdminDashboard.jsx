import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [bots, setBots] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBot, setSelectedBot] = useState(null);

  const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

  useEffect(() => {
    fetchBots();
    fetchLogs();
  }, []);

  const fetchBots = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/bots`);
      setBots(response.data.bots);
    } catch (error) {
      console.error('Error fetching bots:', error);
    }
  };

  const fetchLogs = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/logs`);
      setLogs(response.data.logs);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching logs:', error);
      setLoading(false);
    }
  };

  const triggerBot = async (botId) => {
    try {
      const response = await axios.post(`${API_BASE}/api/bots/${botId}/trigger`);
      alert(response.data.message);
      fetchLogs(); // Refresh logs after triggering
    } catch (error) {
      alert('Error triggering bot: ' + (error.response?.data?.detail || error.message));
    }
  };

  const checkAnomaly = async () => {
    try {
      const rate = Math.random() * 100; // Simulate a rate
      const response = await axios.get(`${API_BASE}/api/security/anomaly-check?rate=${rate}`);
      alert(`Anomaly check result: ${response.data.is_anomalous ? 'ANOMALOUS' : 'NORMAL'} (Rate: ${rate.toFixed(2)})`);
    } catch (error) {
      alert('Error checking anomaly: ' + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return (
      <div className="bg-gray-100 min-h-screen p-6 flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <h2 className="text-3xl font-bold mb-6">Admin Dashboard</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Bots Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">SiteGuardian Bots</h3>
          {bots.length === 0 ? (
            <p className="text-gray-600">No bots configured</p>
          ) : (
            <div className="space-y-4">
              {bots.map((bot) => (
                <div key={bot.id} className="border p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-medium">{bot.name}</h4>
                      <p className="text-sm text-gray-600">{bot.description}</p>
                      <p className="text-sm">
                        Status: <span className={`font-medium ${bot.enabled ? 'text-green-600' : 'text-red-600'}`}>
                          {bot.enabled ? 'Enabled' : 'Disabled'}
                        </span>
                      </p>
                    </div>
                    <button
                      onClick={() => triggerBot(bot.id)}
                      disabled={!bot.enabled}
                      className={`px-3 py-1 rounded text-sm ${
                        bot.enabled 
                          ? 'bg-blue-600 text-white hover:bg-blue-700' 
                          : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      }`}
                    >
                      Trigger
                    </button>
                  </div>
                  <div className="text-sm text-gray-600">
                    <p>Triggers: {bot.triggers.length}</p>
                    <p>Endpoint: {bot.settings.monitor_endpoint}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Security Tools Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Security Tools</h3>
          <div className="space-y-4">
            <button
              onClick={checkAnomaly}
              className="w-full px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition"
            >
              Test Anomaly Detection
            </button>
            <button
              onClick={() => window.open(`${API_BASE}/docs`, '_blank')}
              className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
            >
              API Documentation
            </button>
          </div>
        </div>
      </div>

      {/* Logs Section */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold">Recent Logs</h3>
          <button
            onClick={fetchLogs}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Refresh
          </button>
        </div>
        <div className="bg-gray-900 text-green-400 p-4 rounded-lg h-64 overflow-y-auto font-mono text-sm">
          {logs.length === 0 ? (
            <p>No logs available</p>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="mb-1">
                {log}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;