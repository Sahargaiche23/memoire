import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import './Maintenance.css';

function Maintenance({ user, onLogout }) {
  const [maintenances, setMaintenances] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    asset_id: '',
    maintenance_type: 'préventive',
    scheduled_date: '',
    description: '',
    cost: '',
    status: 'planifiée'
  });

  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      if (!token) {
        console.warn('Pas de token JWT disponible');
        setMaintenances([]);
        setAssets([]);
        setLoading(false);
        return;
      }

      const [mainRes, assetsRes] = await Promise.all([
        axios.get('http://localhost:5000/api/maintenances'),
        axios.get('http://localhost:5000/api/assets')
      ]);
      setMaintenances(mainRes.data || []);
      setAssets(assetsRes.data || []);
    } catch (err) {
      console.error('Erreur:', err);
      if (err.response?.status === 401) {
        console.warn('Token JWT invalide ou expiré');
        // Rediriger vers login ou rafraîchir le token
      }
      setMaintenances([]);
      setAssets([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log('📤 Sauvegarde maintenance:', editingId ? 'Modification' : 'Création');
      console.log('Données:', formData);
      
      if (editingId) {
        const response = await axios.put(
          `http://localhost:5000/api/maintenances/${editingId}`, 
          formData,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        console.log('✅ Réponse modification:', response.data);
        alert('✅ Maintenance modifiée avec succès!');
      } else {
        const response = await axios.post(
          'http://localhost:5000/api/maintenances', 
          formData,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        console.log('✅ Réponse création:', response.data);
        alert('✅ Maintenance créée avec succès!');
      }
      
      fetchData();
      setShowModal(false);
      setFormData({
        asset_id: '',
        maintenance_type: 'préventive',
        scheduled_date: '',
        description: '',
        cost: '',
        status: 'planifiée'
      });
      setEditingId(null);
    } catch (err) {
      console.error('❌ Erreur:', err);
      const errorMsg = err.response?.data?.error || 'Erreur lors de l\'opération';
      alert('❌ ' + errorMsg);
    }
  };

  const handleEdit = (maintenance) => {
    console.log('✏️ Édition maintenance ID:', maintenance.id);
    console.log('Données maintenance:', maintenance);
    
    // S'assurer que tous les champs ont une valeur par défaut
    setFormData({
      asset_id: maintenance.asset_id || '',
      maintenance_type: maintenance.maintenance_type || 'préventive',
      scheduled_date: maintenance.scheduled_date || '',
      description: maintenance.description || '',
      cost: maintenance.cost || '',
      status: maintenance.status || 'planifiée'
    });
    
    setEditingId(maintenance.id);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    console.log('🖱️ Clic sur bouton delete détecté! ID:', id);
    
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette maintenance?')) {
      try {
        console.log('🗑️ Suppression maintenance ID:', id);
        const response = await axios.delete(`http://localhost:5000/api/maintenances/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log('✅ Réponse suppression:', response.data);
        alert('✅ Maintenance supprimée avec succès!');
        fetchData();
      } catch (err) {
        console.error('❌ Erreur suppression:', err);
        const errorMsg = err.response?.data?.error || 'Erreur lors de la suppression';
        alert('❌ ' + errorMsg);
      }
    } else {
      console.log('❌ Suppression annulée par l\'utilisateur');
    }
  };

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="maintenance-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="maintenance-container">
        <div className="maintenance-header">
          <h1>Gestion des Maintenances</h1>
          <button className="btn btn-primary" onClick={() => {
            setEditingId(null);
            setFormData({
              asset_id: '',
              maintenance_type: 'préventive',
              scheduled_date: '',
              description: '',
              cost: '',
              status: 'planifiée'
            });
            setShowModal(true);
          }}>
            <Plus size={18} /> Planifier une maintenance
          </button>
        </div>

        <div className="maintenance-grid">
          {maintenances.map(maintenance => {
            const asset = assets.find(a => a.id === maintenance.asset_id);
            return (
              <div key={maintenance.id} className="maintenance-card">
                <div className="card-header">
                  <h3>{asset?.name || 'Actif inconnu'}</h3>
                  <span className={`badge badge-${maintenance.status === 'complétée' ? 'success' : maintenance.status === 'en_cours' ? 'warning' : 'info'}`}>
                    {maintenance.status}
                  </span>
                </div>
                <div className="card-body">
                  <p><strong>Type:</strong> {maintenance.maintenance_type}</p>
                  <p><strong>Date prévue:</strong> {new Date(maintenance.scheduled_date).toLocaleDateString('fr-TN')}</p>
                  <p><strong>Coût:</strong> {maintenance.cost ? `${maintenance.cost} DT` : 'Non estimé'}</p>
                  <p><strong>Description:</strong> {maintenance.description || 'Aucune description'}</p>
                </div>
                <div className="card-actions">
                  <button className="btn-icon" onClick={() => handleEdit(maintenance)}>
                    <Edit2 size={18} />
                  </button>
                  <button className="btn-icon btn-danger" onClick={() => handleDelete(maintenance.id)}>
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {showModal && (
          <div className="modal active">
            <div className="modal-content">
              <div className="modal-header">
                <h2>{editingId ? 'Modifier la maintenance' : 'Planifier une maintenance'}</h2>
                <button className="close-btn" onClick={() => setShowModal(false)}>×</button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Actif</label>
                  <select name="asset_id" value={formData.asset_id} onChange={handleInputChange} required>
                    <option value="">Sélectionner un actif</option>
                    {assets.map(asset => (
                      <option key={asset.id} value={asset.id}>{asset.name}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Type de maintenance</label>
                  <select name="maintenance_type" value={formData.maintenance_type} onChange={handleInputChange}>
                    <option value="préventive">Préventive</option>
                    <option value="corrective">Corrective</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Date prévue</label>
                  <input
                    type="date"
                    name="scheduled_date"
                    value={formData.scheduled_date}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    name="description"
                    value={formData.description || ''}
                    onChange={handleInputChange}
                    placeholder="Entrez une description de la maintenance..."
                    rows="4"
                  />
                </div>

                <div className="form-group">
                  <label>Coût estimé (DT)</label>
                  <input
                    type="number"
                    name="cost"
                    value={formData.cost || ''}
                    onChange={handleInputChange}
                    placeholder="0.00"
                    step="0.01"
                  />
                </div>

                <div className="form-group">
                  <label>Statut</label>
                  <select name="status" value={formData.status} onChange={handleInputChange}>
                    <option value="planifiée">Planifiée</option>
                    <option value="en_cours">En cours</option>
                    <option value="complétée">Complétée</option>
                  </select>
                </div>

                <div className="modal-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                    Annuler
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingId ? 'Mettre à jour' : 'Créer'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Maintenance;
