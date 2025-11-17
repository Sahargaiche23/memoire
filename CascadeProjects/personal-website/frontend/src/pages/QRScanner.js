import React, { useState } from 'react';
import axios from 'axios';
import { Smartphone, Search, AlertCircle, CheckCircle } from 'lucide-react';
import './QRScanner.css';

function QRScanner() {
  const [qrCode, setQrCode] = useState('');
  const [asset, setAsset] = useState(null);
  const [user, setUser] = useState(null);
  const [scanType, setScanType] = useState('asset'); // 'asset' ou 'user'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleScan = async (e) => {
    e.preventDefault();
    
    if (!qrCode.trim()) {
      setError('Veuillez entrer un code QR');
      return;
    }

    setLoading(true);
    setError('');
    setAsset(null);
    setUser(null);

    try {
      if (scanType === 'asset') {
        const response = await axios.get(
          `http://localhost:5000/api/assets/qr/${qrCode}`
        );
        setAsset(response.data);
      } else {
        const response = await axios.get(
          `http://localhost:5000/api/users/qr/${qrCode}`
        );
        setUser(response.data);
      }
    } catch (err) {
      if (scanType === 'asset') {
        setError('Actif non trouvé. Vérifiez le code QR.');
      } else {
        setError('Utilisateur non trouvé. Vérifiez le code QR.');
      }
      setAsset(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setQrCode('');
    setAsset(null);
    setUser(null);
    setError('');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'actif':
        return '#43e97b';
      case 'maintenance':
        return '#f093fb';
      case 'hors_service':
        return '#fa7231';
      case 'déclassé':
        return '#999';
      default:
        return '#667eea';
    }
  };

  const getStatusLabel = (status) => {
    const labels = {
      'actif': 'Actif',
      'maintenance': 'Maintenance',
      'hors_service': 'Hors Service',
      'déclassé': 'Déclassé'
    };
    return labels[status] || status;
  };

  return (
    <div className="qr-scanner-page">
      <div className="qr-scanner-container">
        <div className="qr-header">
          <Smartphone size={40} />
          <h1>Scanner QR Code</h1>
          <p>Scannez un code QR d'actif ou d'utilisateur</p>
        </div>

        <div className="scan-type-selector">
          <button 
            type="button"
            className={`type-btn ${scanType === 'asset' ? 'active' : ''}`}
            onClick={() => setScanType('asset')}
          >
            🏢 Actifs
          </button>
          <button 
            type="button"
            className={`type-btn ${scanType === 'user' ? 'active' : ''}`}
            onClick={() => setScanType('user')}
          >
            👤 Utilisateurs
          </button>
        </div>

        <div className="qr-form-section">
          <form onSubmit={handleScan} className="qr-form">
            <div className="input-group">
              <input
                type="text"
                value={qrCode}
                onChange={(e) => setQrCode(e.target.value)}
                placeholder="Entrez le code QR ou scannez..."
                className="qr-input"
                autoFocus
              />
              <button type="submit" className="btn-scan" disabled={loading}>
                <Search size={20} />
                {loading ? 'Recherche...' : 'Rechercher'}
              </button>
            </div>
          </form>

          {error && (
            <div className="alert alert-error">
              <AlertCircle size={20} />
              <p>{error}</p>
            </div>
          )}
        </div>

        {asset && (
          <div className="asset-details">
            <div className="asset-header">
              <h2>{asset.name}</h2>
              <span 
                className="status-badge"
                style={{ backgroundColor: getStatusColor(asset.status) }}
              >
                {getStatusLabel(asset.status)}
              </span>
            </div>

            <div className="asset-info-grid">
              <div className="info-card">
                <h3>Catégorie</h3>
                <p>{asset.category}</p>
              </div>

              <div className="info-card">
                <h3>Localisation</h3>
                <p>{asset.location}</p>
              </div>

              <div className="info-card">
                <h3>Affecté à</h3>
                <p>{asset.assigned_to || 'Non affecté'}</p>
              </div>

              <div className="info-card">
                <h3>Date d'Acquisition</h3>
                <p>
                  {asset.acquisition_date 
                    ? new Date(asset.acquisition_date).toLocaleDateString('fr-FR')
                    : 'Non disponible'
                  }
                </p>
              </div>

              <div className="info-card">
                <h3>Valeur d'Acquisition</h3>
                <p>{asset.acquisition_value?.toLocaleString('fr-FR')} DT</p>
              </div>

              <div className="info-card">
                <h3>Valeur Actuelle</h3>
                <p>{asset.current_value?.toLocaleString('fr-FR')} DT</p>
              </div>
            </div>

            <div className="asset-description">
              <h3>Description</h3>
              <p>{asset.description || 'Aucune description'}</p>
            </div>

            <div className="asset-actions">
              <button className="btn-print" onClick={() => window.print()}>
                🖨️ Imprimer
              </button>
              <button className="btn-reset-scan" onClick={handleReset}>
                🔄 Nouveau Scan
              </button>
            </div>

            <div className="success-message">
              <CheckCircle size={20} />
              <p>Informations de l'actif chargées avec succès</p>
            </div>
          </div>
        )}

        {user && (
          <div className="user-details">
            <div className="user-header">
              <h2>{user.full_name}</h2>
              <span className="role-badge">{user.role}</span>
            </div>

            <div className="user-info-grid">
              <div className="info-card">
                <h3>Nom d'utilisateur</h3>
                <p>@{user.username}</p>
              </div>

              <div className="info-card">
                <h3>Email</h3>
                <p>{user.email}</p>
              </div>

              <div className="info-card">
                <h3>Rôle</h3>
                <p>{user.role}</p>
              </div>

              <div className="info-card">
                <h3>Code QR</h3>
                <p className="qr-code-display">{user.qr_code}</p>
              </div>

              <div className="info-card">
                <h3>Créé le</h3>
                <p>
                  {user.created_at 
                    ? new Date(user.created_at).toLocaleDateString('fr-FR')
                    : 'Non disponible'
                  }
                </p>
              </div>
            </div>

            <div className="user-actions">
              <button className="btn-print" onClick={() => window.print()}>
                🖨️ Imprimer
              </button>
              <button className="btn-reset-scan" onClick={handleReset}>
                🔄 Nouveau Scan
              </button>
            </div>

            <div className="success-message">
              <CheckCircle size={20} />
              <p>Informations de l'utilisateur chargées avec succès</p>
            </div>
          </div>
        )}

        {!asset && !user && !error && (
          <div className="empty-state">
            <Smartphone size={60} />
            <h3>Prêt à scanner</h3>
            <p>Entrez un code QR pour voir les détails {scanType === 'asset' ? 'de l\'actif' : 'de l\'utilisateur'}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default QRScanner;
