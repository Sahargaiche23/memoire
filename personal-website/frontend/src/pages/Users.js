import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import './Users.css';

function Users({ user, onLogout }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'user'
  });

  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/users', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data);
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
      if (isRegistering) {
        const response = await axios.post('http://localhost:5000/api/auth/register', formData);
        if (response.status === 201) {
          const userData = response.data.user;
          alert(`✅ Utilisateur créé avec succès!\n\n` +
                `👤 Nom d'utilisateur: ${userData.username}\n` +
                `📧 Email: ${userData.email}\n` +
                `🎫 QR Code: ${userData.qr_code}\n` +
                `👥 Rôle: ${userData.role}\n\n` +
                `🔐 Mot de passe: ${formData.password}\n\n` +
                `L'utilisateur peut maintenant:\n` +
                `• Se connecter avec son username/password\n` +
                `• Voir son QR code unique dans son profil\n` +
                `• Scanner des QR codes`);
          console.log('✅ Nouvel utilisateur créé:', userData);
        }
      } else {
        await axios.put(`http://localhost:5000/api/users/${editingId}`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('✅ Utilisateur mis à jour avec succès!');
      }
      fetchUsers();
      setShowModal(false);
      setFormData({
        username: '',
        email: '',
        password: '',
        full_name: '',
        role: 'user'
      });
      setEditingId(null);
      setIsRegistering(false);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Erreur lors de l\'opération';
      alert('❌ ' + errorMsg);
      console.error('Erreur:', err);
    }
  };

  const handleEdit = (userData) => {
    setFormData(userData);
    setEditingId(userData.id);
    setIsRegistering(false);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur?')) {
      try {
        console.log('🗑️ Suppression utilisateur ID:', id);
        const response = await axios.delete(`http://localhost:5000/api/users/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log('✅ Réponse suppression:', response.data);
        alert('✅ Utilisateur supprimé avec succès!');
        fetchUsers();
      } catch (err) {
        console.error('❌ Erreur suppression:', err);
        const errorMsg = err.response?.data?.error || 'Erreur lors de la suppression';
        alert('❌ ' + errorMsg);
      }
    }
  };

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="users-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="users-container">
        <div className="users-header">
          <h1>Gestion des Utilisateurs</h1>
          <button className="btn btn-primary" onClick={() => {
            setEditingId(null);
            setIsRegistering(true);
            setFormData({
              username: '',
              email: '',
              password: '',
              full_name: '',
              role: 'user'
            });
            setShowModal(true);
          }}>
            <Plus size={18} /> Ajouter un utilisateur
          </button>
        </div>

        <div className="users-table-container">
          <table className="users-table">
            <thead>
              <tr>
                <th>Nom d'utilisateur</th>
                <th>Email</th>
                <th>Nom complet</th>
                <th>Rôle</th>
                <th>QR Code</th>
                <th>Date création</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(userData => (
                <tr key={userData.id}>
                  <td><strong>{userData.username}</strong></td>
                  <td>{userData.email}</td>
                  <td>{userData.full_name}</td>
                  <td>
                    <span className="badge badge-info">{userData.role}</span>
                  </td>
                  <td>
                    {userData.qr_code ? (
                      <code className="qr-code-badge">{userData.qr_code}</code>
                    ) : (
                      <span className="text-muted">-</span>
                    )}
                  </td>
                  <td>{new Date(userData.created_at).toLocaleDateString('fr-TN')}</td>
                  <td className="actions">
                    <button className="btn-icon" onClick={() => handleEdit(userData)}>
                      <Edit2 size={18} />
                    </button>
                    <button className="btn-icon btn-danger" onClick={() => handleDelete(userData.id)}>
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
                <h2>{isRegistering ? 'Ajouter un utilisateur' : 'Modifier l\'utilisateur'}</h2>
                <button className="close-btn" onClick={() => setShowModal(false)}>×</button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Nom d'utilisateur</label>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleInputChange}
                    required
                    disabled={!isRegistering}
                  />
                </div>

                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                {isRegistering && (
                  <div className="form-group">
                    <label>Mot de passe</label>
                    <input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                )}

                <div className="form-group">
                  <label>Nom complet</label>
                  <input
                    type="text"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="form-group">
                  <label>Rôle</label>
                  <select name="role" value={formData.role} onChange={handleInputChange}>
                    <option value="user">Utilisateur</option>
                    <option value="admin">Administrateur</option>
                    <option value="responsable_patrimoine">Responsable Patrimoine</option>
                    <option value="responsable_service">Responsable Service</option>
                    <option value="agent_maintenance">Agent Maintenance</option>
                    <option value="auditeur">Auditeur</option>
                  </select>
                </div>

                <div className="modal-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                    Annuler
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {isRegistering ? 'Créer' : 'Mettre à jour'}
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

export default Users;
