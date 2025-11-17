import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Download, Share2, QrCode, Eye } from 'lucide-react';
import './QRGallery.css';

function QRGallery({ user, onLogout }) {
  const [qrCodes, setQrCodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchQRCodes();
  }, []);

  const fetchQRCodes = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/qr-codes');
      setQrCodes(response.data);
    } catch (err) {
      console.error('Erreur:', err);
      setError('Erreur lors du chargement des QR codes');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (qrCode) => {
    const link = document.createElement('a');
    link.href = `http://localhost:5000${qrCode.qr_image_url}`;
    link.download = `qr_${qrCode.username}_${qrCode.qr_code}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleShare = async (qrCode) => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `QR Code - ${qrCode.full_name}`,
          text: `Scannez mon QR code: ${qrCode.qr_code}`,
          url: qrCode.scan_url
        });
      } catch (err) {
        console.log('Partage annulé');
      }
    } else {
      // Fallback: copier l'URL
      navigator.clipboard.writeText(qrCode.scan_url);
      alert('URL copiée dans le presse-papiers!');
    }
  };

  const handleViewScanner = (qrCode) => {
    window.open(qrCode.scan_url, '_blank');
  };

  if (loading) {
    return (
      <div className="qr-gallery-page">
        <Navbar user={user} onLogout={onLogout} />
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Chargement des QR codes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="qr-gallery-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="qr-gallery-container">
        <div className="gallery-header">
          <QrCode size={48} />
          <h1>🎨 Galerie QR Codes</h1>
          <p>Vos QR codes personnalisés pour le système de patrimoine municipal</p>
          
          <div className="stats-bar">
            <div className="stat-item">
              <span className="stat-number">{qrCodes.length}</span>
              <span className="stat-label">QR Codes</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">100%</span>
              <span className="stat-label">Scannables</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">HD</span>
              <span className="stat-label">Qualité</span>
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        <div className="qr-grid">
          {qrCodes.map((qrCode, index) => (
            <div key={qrCode.username} className="qr-card">
              <div className="qr-image-container">
                <img 
                  src={`http://localhost:5000${qrCode.qr_image_url}`}
                  alt={`QR Code ${qrCode.full_name}`}
                  className="qr-image"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
                <div className="qr-placeholder" style={{display: 'none'}}>
                  <QrCode size={60} />
                  <p>Image non disponible</p>
                </div>
              </div>
              
              <div className="qr-info">
                <h3 className="user-name">{qrCode.full_name}</h3>
                <p className="username">@{qrCode.username}</p>
                <div className="qr-code-display">
                  <span className="code-label">Code:</span>
                  <span className="code-value">{qrCode.qr_code}</span>
                </div>
              </div>
              
              <div className="qr-actions">
                <button 
                  className="action-btn primary"
                  onClick={() => handleViewScanner(qrCode)}
                  title="Tester le scan"
                >
                  <Eye size={16} />
                  Scanner
                </button>
                
                <button 
                  className="action-btn secondary"
                  onClick={() => handleDownload(qrCode)}
                  title="Télécharger l'image"
                >
                  <Download size={16} />
                  Télécharger
                </button>
                
                <button 
                  className="action-btn tertiary"
                  onClick={() => handleShare(qrCode)}
                  title="Partager"
                >
                  <Share2 size={16} />
                  Partager
                </button>
              </div>
            </div>
          ))}
        </div>

        {qrCodes.length === 0 && !loading && !error && (
          <div className="empty-state">
            <QrCode size={80} />
            <h3>Aucun QR code trouvé</h3>
            <p>Générez vos QR codes avec le script backend</p>
          </div>
        )}

        <div className="gallery-footer">
          <div className="info-section">
            <h3>💡 Comment utiliser vos QR codes</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-icon">📱</span>
                <div>
                  <h4>Scanner</h4>
                  <p>Utilisez l'appareil photo ou allez sur /qr-scanner</p>
                </div>
              </div>
              
              <div className="info-item">
                <span className="info-icon">🖨️</span>
                <div>
                  <h4>Imprimer</h4>
                  <p>Téléchargez et imprimez pour un usage physique</p>
                </div>
              </div>
              
              <div className="info-item">
                <span className="info-icon">🔗</span>
                <div>
                  <h4>Partager</h4>
                  <p>Envoyez le lien direct pour un scan rapide</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default QRGallery;
