import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Plus, Edit2, Trash2, Search } from 'lucide-react';
import './Assets.css';

function Assets({ user, onLogout }) {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    category: 'bâtiment',
    description: '',
    acquisition_date: '',
    acquisition_value: '',
    current_value: '',
    location: '',
    status: 'actif',
    assigned_to: ''
  });

  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/assets', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAssets(response.data);
    } catch (err) {
      console.error('Erreur:', err);
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
      if (editingId) {
        await axios.put(`http://localhost:5000/api/assets/${editingId}`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post('http://localhost:5000/api/assets', formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      fetchAssets();
      setShowModal(false);
      setFormData({
        name: '',
        category: 'bâtiment',
        description: '',
        acquisition_date: '',
        acquisition_value: '',
        current_value: '',
        location: '',
        status: 'actif',
        assigned_to: ''
      });
      setEditingId(null);
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const handleEdit = (asset) => {
    setFormData(asset);
    setEditingId(asset.id);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr?')) {
      try {
        await axios.delete(`http://localhost:5000/api/assets/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchAssets();
      } catch (err) {
        console.error('Erreur:', err);
      }
    }
  };

  const filteredAssets = assets.filter(asset =>
    asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    asset.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="assets-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="assets-container">
        <div className="assets-header">
          <h1>Gestion des Actifs</h1>
          <button className="btn btn-primary" onClick={() => {
            setEditingId(null);
            setFormData({
              name: '',
              category: 'bâtiment',
              description: '',
              acquisition_date: '',
              acquisition_value: '',
              current_value: '',
              location: '',
              status: 'actif',
              assigned_to: ''
            });
            setShowModal(true);
          }}>
            <Plus size={18} /> Ajouter un actif
          </button>
        </div>

        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Rechercher un actif..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="assets-table-container">
          <table className="assets-table">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Catégorie</th>
                <th>Localisation</th>
                <th>Valeur Actuelle</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAssets.map(asset => (
                <tr key={asset.id}>
                  <td><strong>{asset.name}</strong></td>
                  <td>{asset.category}</td>
                  <td>{asset.location}</td>
                  <td>{asset.current_value?.toLocaleString('fr-TN')} DT</td>
                  <td>
                    <span className={`badge badge-${asset.status === 'actif' ? 'success' : 'warning'}`}>
                      {asset.status}
                    </span>
                  </td>
                  <td className="actions">
                    <button className="btn-icon" onClick={() => handleEdit(asset)}>
                      <Edit2 size={18} />
                    </button>
                    <button className="btn-icon btn-danger" onClick={() => handleDelete(asset.id)}>
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {showModal && (
          <div className="modal active">
            <div className="modal-content">
              <div className="modal-header">
                <h2>{editingId ? 'Modifier l\'actif' : 'Ajouter un actif'}</h2>
                <button className="close-btn" onClick={() => setShowModal(false)}>×</button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Nom</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Catégorie</label>
                  <select name="category" value={formData.category} onChange={handleInputChange}>
                    <option value="bâtiment">Bâtiment</option>
                    <option value="véhicule">Véhicule</option>
                    <option value="équipement">Équipement</option>
                    <option value="mobilier">Mobilier</option>
                    <option value="terrain">Terrain</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Date d'acquisition</label>
                    <input
                      type="date"
                      name="acquisition_date"
                      value={formData.acquisition_date}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Valeur d'acquisition</label>
                    <input
                      type="number"
                      name="acquisition_value"
                      value={formData.acquisition_value}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Valeur actuelle</label>
                    <input
                      type="number"
                      name="current_value"
                      value={formData.current_value}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Localisation</label>
                    <input
                      type="text"
                      name="location"
                      value={formData.location}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Statut</label>
                    <select name="status" value={formData.status} onChange={handleInputChange}>
                      <option value="actif">Actif</option>
                      <option value="maintenance">Maintenance</option>
                      <option value="hors_service">Hors service</option>
                      <option value="déclassé">Déclassé</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Assigné à</label>
                    <input
                      type="text"
                      name="assigned_to"
                      value={formData.assigned_to}
                      onChange={handleInputChange}
                    />
                  </div>
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

export default Assets;
