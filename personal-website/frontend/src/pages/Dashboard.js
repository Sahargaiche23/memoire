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
    
    // Auto-refresh toutes les 30 secondes pour les alertes dynamiques
    const interval = setInterval(() => {
      fetchAlerts();
    }, 30000);
    
    return () => clearInterval(interval);
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
      setAlerts(alertsRes.data);
      console.log('✅ Données chargées:', alertsRes.data.length, 'alerte(s)');
    } catch (err) {
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchAlerts = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/alerts', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAlerts(res.data);
      console.log('🔄 Alertes actualisées:', res.data.length);
    } catch (err) {
      console.error('Erreur actualisation alertes:', err);
    }
  };
  
  const markAlertAsRead = async (alertId) => {
    // Toutes les alertes sont maintenant stockées en BDD et peuvent être marquées
    try {
      await axios.put(`http://localhost:5000/api/alerts/${alertId}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Mettre à jour l'état local
      setAlerts(prev => prev.map(alert => 
        alert.id === alertId ? { ...alert, is_read: true } : alert
      ));
      
      console.log('✅ Alerte marquée comme lue:', alertId);
    } catch (err) {
      console.error('Erreur marquer alerte:', err);
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
          <div className="alerts-header">
            <h2>Alertes Récentes</h2>
            <button className="refresh-btn" onClick={fetchAlerts} title="Actualiser">
              🔄
            </button>
          </div>
          <div className="alerts-list">
            {alerts.length > 0 ? (
              alerts.map(alert => {
                // Toutes les alertes peuvent maintenant être marquées comme lues
                const isClickable = !alert.is_read;
                
                // Badge de priorité
                const getPriorityBadge = (priority) => {
                  const badges = {
                    'CRITICAL': { emoji: '🚨', color: '#ef4444', text: 'Critique' },
                    'HIGH': { emoji: '⚠️', color: '#f59e0b', text: 'Haute' },
                    'MEDIUM': { emoji: '🔧', color: '#3b82f6', text: 'Moyenne' }
                  };
                  return badges[priority] || badges['MEDIUM'];
                };
                
                const priorityBadge = getPriorityBadge(alert.priority);
                
                return (
                <div 
                  key={alert.id} 
                  className={`alert-item ${alert.is_read ? 'read' : 'unread'} priority-${alert.priority?.toLowerCase()}`}
                  onClick={() => isClickable && markAlertAsRead(alert.id)}
                  style={{ cursor: isClickable ? 'pointer' : 'default' }}
                  title={isClickable ? 'Cliquez pour marquer comme lue' : ''}
                >
                  <div className="alert-icon" style={{ color: priorityBadge.color }}>
                    <span style={{ fontSize: '24px' }}>{priorityBadge.emoji}</span>
                  </div>
                  <div className="alert-content">
                    <div className="alert-header">
                      <h4>{alert.alert_type}</h4>
                      <span className="priority-badge" style={{ 
                        background: priorityBadge.color,
                        color: 'white',
                        padding: '2px 8px',
                        borderRadius: '12px',
                        fontSize: '11px',
                        fontWeight: 'bold'
                      }}>
                        {priorityBadge.text}
                      </span>
                    </div>
                    <p>{alert.message}</p>
                    <div className="alert-meta">
                      <span className="alert-date">
                        {new Date(alert.created_at).toLocaleDateString('fr-TN', {
                          day: '2-digit',
                          month: 'short',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </span>
                      {alert.days_count && (
                        <span className="alert-days" style={{ 
                          marginLeft: '10px',
                          fontWeight: 'bold',
                          color: priorityBadge.color 
                        }}>
                          {alert.alert_type === 'MAINTENANCE_LATE' 
                            ? `${alert.days_count}j de retard` 
                            : `${alert.days_count}j restants`
                          }
                        </span>
                      )}
                    </div>
                  </div>
                  <span className={`alert-status ${alert.is_read ? 'read' : 'unread'}`}>
                    {alert.is_read ? '✓ Lue' : '● Non lue'}
                  </span>
                </div>
                );
              })
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
