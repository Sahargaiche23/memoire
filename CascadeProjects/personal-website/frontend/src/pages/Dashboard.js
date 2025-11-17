import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, TrendingUp, Package, Wrench } from 'lucide-react';
import './Dashboard.css';

function Dashboard({ user, onLogout }) {
  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, alertsRes] = await Promise.all([
        axios.get('http://localhost:5000/api/statistics', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/api/alerts', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      setStats(statsRes.data);
      setAlerts(alertsRes.data.slice(0, 5));
    } catch (err) {
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="dashboard">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Tableau de Bord</h1>
          <p>Bienvenue, {user?.full_name || user?.username}!</p>
        </div>

        {/* Stats Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#667eea' }}>
              <Package size={24} color="white" />
            </div>
            <h3>Actifs Total</h3>
            <div className="value">{stats?.total_assets || 0}</div>
            <p className="stat-subtitle">Actifs enregistrés</p>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#764ba2' }}>
              <TrendingUp size={24} color="white" />
            </div>
            <h3>Actifs Actifs</h3>
            <div className="value">{stats?.active_assets || 0}</div>
            <p className="stat-subtitle">En service</p>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#f093fb' }}>
              <Wrench size={24} color="white" />
            </div>
            <h3>Valeur Totale</h3>
            <div className="value">{(stats?.total_value || 0).toLocaleString('fr-TN')} DT</div>
            <p className="stat-subtitle">Patrimoine municipal</p>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#4facfe' }}>
              <AlertCircle size={24} color="white" />
            </div>
            <h3>Alertes</h3>
            <div className="value">{alerts.length}</div>
            <p className="stat-subtitle">À traiter</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="charts-section">
          <div className="chart-card">
            <h2>Distribution par Catégorie</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats?.by_category || []}
                  dataKey="count"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {(stats?.by_category || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h2>Actifs par Catégorie</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats?.by_category || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alerts Section */}
        <div className="alerts-section">
          <h2>Alertes Récentes</h2>
          <div className="alerts-list">
            {alerts.length > 0 ? (
              alerts.map(alert => (
                <div key={alert.id} className="alert-item">
                  <div className="alert-icon">
                    <AlertCircle size={20} />
                  </div>
                  <div className="alert-content">
                    <h4>{alert.alert_type}</h4>
                    <p>{alert.message}</p>
                    <span className="alert-date">
                      {new Date(alert.created_at).toLocaleDateString('fr-TN')}
                    </span>
                  </div>
                  <span className={`alert-status ${alert.is_read ? 'read' : 'unread'}`}>
                    {alert.is_read ? 'Lue' : 'Non lue'}
                  </span>
                </div>
              ))
            ) : (
              <p className="no-alerts">Aucune alerte</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
