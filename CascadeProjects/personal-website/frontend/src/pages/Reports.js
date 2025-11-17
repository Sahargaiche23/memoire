import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Download, BarChart3 } from 'lucide-react';
import './Reports.css';

function Reports({ user, onLogout }) {
  const [stats, setStats] = useState(null);
  const [assets, setAssets] = useState([]);
  const [maintenances, setMaintenances] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, assetsRes, mainRes] = await Promise.all([
        axios.get('http://localhost:5000/api/statistics', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/api/assets', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/api/maintenances', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      setStats(statsRes.data);
      setAssets(assetsRes.data);
      setMaintenances(mainRes.data);
    } catch (err) {
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const generatePDF = () => {
    const doc = `
RAPPORT DE GESTION DU PATRIMOINE MUNICIPAL
Généré le: ${new Date().toLocaleDateString('fr-TN')}

=== STATISTIQUES GÉNÉRALES ===
Total des actifs: ${stats?.total_assets || 0}
Actifs actifs: ${stats?.active_assets || 0}
Valeur totale du patrimoine: ${(stats?.total_value || 0).toLocaleString('fr-TN')} DT

=== DISTRIBUTION PAR CATÉGORIE ===
${stats?.by_category?.map(cat => `${cat.category}: ${cat.count} actifs`).join('\n')}

=== DÉTAILS DES ACTIFS ===
${assets.map(a => `
Nom: ${a.name}
Catégorie: ${a.category}
Localisation: ${a.location}
Valeur actuelle: ${a.current_value} DT
Statut: ${a.status}
Date d'acquisition: ${a.acquisition_date}
---`).join('\n')}

=== MAINTENANCES PLANIFIÉES ===
${maintenances.map(m => `
Type: ${m.maintenance_type}
Date prévue: ${m.scheduled_date}
Coût: ${m.cost} DT
Statut: ${m.status}
---`).join('\n')}
    `;

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(doc));
    element.setAttribute('download', `rapport_patrimoine_${new Date().getTime()}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const generateCSV = () => {
    let csv = 'Nom,Catégorie,Localisation,Valeur Actuelle,Statut,Date Acquisition\n';
    csv += assets.map(a => 
      `"${a.name}","${a.category}","${a.location}","${a.current_value}","${a.status}","${a.acquisition_date}"`
    ).join('\n');

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
    element.setAttribute('download', `actifs_${new Date().getTime()}.csv`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="reports-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="reports-container">
        <div className="reports-header">
          <h1>Rapports et Statistiques</h1>
          <div className="export-buttons">
            <button className="btn btn-primary" onClick={generatePDF}>
              <Download size={18} /> Exporter en PDF
            </button>
            <button className="btn btn-primary" onClick={generateCSV}>
              <Download size={18} /> Exporter en CSV
            </button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="summary-grid">
          <div className="summary-card">
            <h3>Total des Actifs</h3>
            <div className="summary-value">{stats?.total_assets || 0}</div>
          </div>
          <div className="summary-card">
            <h3>Actifs Actifs</h3>
            <div className="summary-value">{stats?.active_assets || 0}</div>
          </div>
          <div className="summary-card">
            <h3>Valeur Totale</h3>
            <div className="summary-value">{(stats?.total_value || 0).toLocaleString('fr-TN')} DT</div>
          </div>
          <div className="summary-card">
            <h3>Maintenances</h3>
            <div className="summary-value">{maintenances.length}</div>
          </div>
        </div>

        {/* Category Distribution */}
        <div className="report-section">
          <h2>Distribution par Catégorie</h2>
          <div className="category-list">
            {stats?.by_category?.map((cat, idx) => (
              <div key={idx} className="category-item">
                <span className="category-name">{cat.category}</span>
                <div className="category-bar">
                  <div 
                    className="category-fill" 
                    style={{ 
                      width: `${(cat.count / (stats?.total_assets || 1)) * 100}%` 
                    }}
                  ></div>
                </div>
                <span className="category-count">{cat.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Assets Table */}
        <div className="report-section">
          <h2>Liste Complète des Actifs</h2>
          <div className="table-container">
            <table className="report-table">
              <thead>
                <tr>
                  <th>Nom</th>
                  <th>Catégorie</th>
                  <th>Localisation</th>
                  <th>Valeur Acquisition</th>
                  <th>Valeur Actuelle</th>
                  <th>Statut</th>
                  <th>Date Acquisition</th>
                </tr>
              </thead>
              <tbody>
                {assets.map(asset => (
                  <tr key={asset.id}>
                    <td>{asset.name}</td>
                    <td>{asset.category}</td>
                    <td>{asset.location}</td>
                    <td>{asset.acquisition_value?.toLocaleString('fr-TN')} DT</td>
                    <td>{asset.current_value?.toLocaleString('fr-TN')} DT</td>
                    <td>
                      <span className={`badge badge-${asset.status === 'actif' ? 'success' : 'warning'}`}>
                        {asset.status}
                      </span>
                    </td>
                    <td>{asset.acquisition_date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Maintenance Report */}
        <div className="report-section">
          <h2>Rapport des Maintenances</h2>
          <div className="table-container">
            <table className="report-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Date Prévue</th>
                  <th>Date Complétée</th>
                  <th>Coût</th>
                  <th>Statut</th>
                </tr>
              </thead>
              <tbody>
                {maintenances.map(m => (
                  <tr key={m.id}>
                    <td>{m.maintenance_type}</td>
                    <td>{m.scheduled_date}</td>
                    <td>{m.completed_date || '-'}</td>
                    <td>{m.cost} DT</td>
                    <td>
                      <span className={`badge badge-${m.status === 'complétée' ? 'success' : 'warning'}`}>
                        {m.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Reports;
