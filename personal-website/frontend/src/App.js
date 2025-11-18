import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import setupAxiosInterceptors from './utils/axiosConfig';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import Maintenance from './pages/Maintenance';
import Users from './pages/Users';
import Reports from './pages/Reports';
import Messages from './pages/Messages';
import Messenger from './pages/Messenger';
import Chatbot from './pages/Chatbot';
import QRScanner from './pages/QRScanner';
import Profile from './pages/Profile';
import AssetSearch from './pages/AssetSearch';
import QRGallery from './pages/QRGallery';
import './App.css';
import './global-buttons-fix.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Configurer les intercepteurs Axios
    setupAxiosInterceptors();
    
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  const updateUser = (updatedData) => {
    // Mettre à jour le state user avec les nouvelles données
    const updatedUser = { ...user, ...updatedData };
    setUser(updatedUser);
    // Mettre à jour localStorage pour persister les changements
    localStorage.setItem('user', JSON.stringify(updatedUser));
    console.log('✅ User mis à jour dans App.js:', updatedUser);
  };

  if (loading) {
    return <div className="loading">Chargement...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/dashboard" />} 
        />
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <Dashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/assets" 
          element={isAuthenticated ? <Assets user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/maintenance" 
          element={isAuthenticated ? <Maintenance user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/users" 
          element={isAuthenticated ? <Users user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/reports" 
          element={isAuthenticated ? <Reports user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/messages" 
          element={isAuthenticated ? <Messages user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/messenger" 
          element={isAuthenticated ? <Messenger user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/chatbot" 
          element={isAuthenticated ? <Chatbot user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/qr-scanner" 
          element={<QRScanner />} 
        />
        <Route 
          path="/profile" 
          element={isAuthenticated ? <Profile user={user} token={localStorage.getItem('token')} onLogout={handleLogout} updateUser={updateUser} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/search-assets" 
          element={isAuthenticated ? <AssetSearch user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/qr-gallery" 
          element={isAuthenticated ? <QRGallery user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;
