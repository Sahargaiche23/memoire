import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { User, Mail, Shield, Calendar, QrCode, Download, Copy, Camera, Edit, Save, X } from 'lucide-react';
import './Profile.css';

function Profile({ user, token, onLogout, updateUser }) {
  const [qrImage, setQrImage] = useState(null);
  const [copied, setCopied] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showCameraScanner, setShowCameraScanner] = useState(false);
  const [profileImage, setProfileImage] = useState(null);
  const [editData, setEditData] = useState({
    full_name: '',
    email: ''
  });
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);

  // Synchroniser editData avec user
  useEffect(() => {
    if (user) {
      setEditData({
        full_name: user.full_name || '',
        email: user.email || ''
      });
      
      // Charger l'image de profil si elle existe (Base64)
      if (user.profile_image) {
        // L'image est déjà en format Data URL (data:image/...;base64,...)
        setProfileImage(user.profile_image);
        console.log('✅ Image de profil (Base64) chargée');
      }
    }
  }, [user]);

  useEffect(() => {
    console.log('🔄 useEffect appelé - User:', user);
    
    const generateQRCode = async (qrCode) => {
      console.log('🎨 Génération QR Code pour:', qrCode);
      console.log('Username:', user?.username);
      
      try {
        // Vérifier d'abord si le fichier local existe
        const localQrUrl = `http://localhost:5000/qr_codes/qr_${user.username}_${qrCode}.png`;
        console.log('🔍 Test fichier local:', localQrUrl);
        
        // Essayer de charger l'image locale
        const img = new Image();
        img.onload = () => {
          console.log('✅ QR local trouvé!');
          setQrImage(localQrUrl);
        };
        img.onerror = () => {
          console.log('⚠️ QR local non trouvé, utilisation API externe');
          const fallbackUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${qrCode}`;
          console.log('🌐 URL fallback:', fallbackUrl);
          setQrImage(fallbackUrl);
        };
        img.src = localQrUrl;
        
      } catch (error) {
        console.error('❌ Erreur génération QR:', error);
        const fallbackUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${qrCode}`;
        console.log('🌐 Utilisation API externe:', fallbackUrl);
        setQrImage(fallbackUrl);
      }
    };
    
    // Générer l'image QR code
    if (user?.qr_code) {
      console.log('✅ QR Code trouvé:', user.qr_code);
      generateQRCode(user.qr_code);
    } else {
      console.log('❌ Pas de QR code pour cet utilisateur');
    }
  }, [user]);

  const downloadQR = async () => {
    console.log('🔽 Fonction downloadQR appelée');
    console.log('QR Image URL:', qrImage);
    console.log('Username:', user?.username);
    
    if (!qrImage) {
      alert('❌ Aucune image QR disponible');
      return;
    }
    
    if (!user?.username) {
      alert('❌ Nom d\'utilisateur non disponible');
      return;
    }
    
    try {
      console.log('📥 Début du téléchargement...');
      const response = await fetch(qrImage);
      console.log('Response status:', response.status);
      
      const blob = await response.blob();
      console.log('Blob size:', blob.size);
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${user.username}_qr_code.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      console.log('✅ Téléchargement réussi!');
      alert(`✅ QR Code téléchargé avec succès!\nFichier: ${user.username}_qr_code.png`);
    } catch (error) {
      console.error('❌ Erreur téléchargement:', error);
      alert(`❌ Erreur lors du téléchargement:\n${error.message}`);
    }
  };

  const copyQRCode = async () => {
    console.log('📋 Fonction copyQRCode appelée');
    console.log('QR Code:', user?.qr_code);
    
    if (!user?.qr_code) {
      alert('❌ Aucun code QR disponible');
      return;
    }
    
    try {
      await navigator.clipboard.writeText(user.qr_code);
      console.log('✅ Copie réussie!');
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      alert(`✅ Code QR copié dans le presse-papier!\nCode: ${user.qr_code}`);
    } catch (error) {
      console.error('❌ Erreur copie:', error);
      alert(`❌ Erreur lors de la copie:\n${error.message}`);
    }
  };

  const testScanner = () => {
    console.log('🧪 Fonction testScanner appelée');
    console.log('QR Code:', user?.qr_code);
    
    if (!user?.qr_code) {
      alert('❌ Aucun code QR disponible');
      return;
    }
    
    const scannerUrl = `/qr-scanner?code=${user.qr_code}`;
    console.log('Ouverture de:', scannerUrl);
    
    const newWindow = window.open(scannerUrl, '_blank');
    
    if (newWindow) {
      console.log('✅ Fenêtre ouverte avec succès');
      alert(`✅ Scanner ouvert dans un nouvel onglet!\nCode: ${user.qr_code}`);
    } else {
      console.log('❌ Fenêtre bloquée par le navigateur');
      alert('❌ Popup bloqué. Autorisez les pop-ups pour ce site.');
    }
  };

  const handleProfileImageChange = async (e) => {
    console.log('📸 Fonction handleProfileImageChange appelée');
    const file = e.target.files[0];
    
    if (!file) {
      console.log('❌ Aucun fichier sélectionné');
      return;
    }
    
    console.log('Fichier:', file.name, 'Size:', file.size, 'bytes');
    
    if (file.size > 5 * 1024 * 1024) {
      alert('❌ L\'image ne doit pas dépasser 5MB');
      return;
    }
    
    // Upload vers le backend avec sauvegarde en base de données
    const formData = new FormData();
    formData.append('file', file);
    console.log('📤 Upload vers backend avec sauvegarde en Base64...');
      
    try {
      const response = await axios.post(
        `http://localhost:5000/api/users/${user.id}/profile-image`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      console.log('✅ Upload réussi (Base64):', response.data);
      
      // Récupérer l'image Base64 depuis la réponse du backend
      if (response.data.profile_image) {
        const base64Image = response.data.profile_image;
        // Mettre à jour l'affichage immédiatement
        setProfileImage(base64Image);
        // Mettre à jour le user dans App.js (state global + localStorage)
        updateUser({ profile_image: base64Image });
        console.log('✅ Image mise à jour dans l\'affichage (Base64)');
        console.log('   Taille Base64:', base64Image.length, 'caractères');
      }
      
      alert(`✅ Photo de profil uploadée et sauvegardée!\nTaille: ${response.data.image_size} bytes\nBase64: ${response.data.base64_size} chars`);
      
    } catch (error) {
      console.error('❌ Erreur upload:', error);
      alert('❌ Erreur lors de l\'upload: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleSaveProfile = async () => {
    console.log('💾 Fonction handleSaveProfile appelée');
    console.log('Données à sauvegarder:', editData);
    console.log('User ID:', user?.id);
    console.log('Token présent:', !!token);
    
    if (!editData.full_name.trim()) {
      alert('❌ Le nom complet est requis');
      return;
    }
    
    if (!editData.email.trim()) {
      alert('❌ L\'email est requis');
      return;
    }
    
    // Validation email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(editData.email)) {
      alert('❌ Email invalide');
      return;
    }
    
    try {
      const response = await axios.put(
        `http://localhost:5000/api/users/${user.id}`,
        {
          full_name: editData.full_name,
          email: editData.email
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      
      console.log('✅ Mise à jour réussie:', response.data);
      
      // Mettre à jour le user dans App.js (state global + localStorage)
      updateUser({
        full_name: editData.full_name,
        email: editData.email
      });
      
      console.log('✅ Données utilisateur mises à jour dans App.js');
      
      alert('✅ Profil mis à jour avec succès!\n\n' +
            `Nom: ${editData.full_name}\n` +
            `Email: ${editData.email}`);
      
      setShowEditModal(false);
      
    } catch (error) {
      console.error('Erreur mise à jour:', error);
      alert('❌ Erreur lors de la mise à jour du profil' + '\n' + 
            (error.response?.data?.error || error.message));
    }
  };

  const startCameraScanner = async () => {
    console.log('📷 Fonction startCameraScanner appelée');
    
    try {
      console.log('🎥 Demande d\'accès à la caméra...');
      setShowCameraScanner(true);
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      console.log('✅ Accès caméra accordé');
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error('❌ Erreur caméra:', error);
      alert(`❌ Impossible d\'accéder à la caméra.\nErreur: ${error.message}\n\nVérifiez les permissions caméra dans votre navigateur.`);
      setShowCameraScanner(false);
    }
  };

  const stopCameraScanner = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
    setShowCameraScanner(false);
  };

  const getRoleColor = (role) => {
    const colors = {
      admin: '#667eea',
      responsable_patrimoine: '#764ba2',
      responsable_service: '#f093fb',
      agent_maintenance: '#4facfe',
      auditeur: '#43e97b'
    };
    return colors[role] || '#667eea';
  };

  const getRoleLabel = (role) => {
    const labels = {
      admin: 'Administrateur',
      responsable_patrimoine: 'Responsable Patrimoine',
      responsable_service: 'Responsable Service',
      agent_maintenance: 'Agent Maintenance',
      auditeur: 'Auditeur'
    };
    return labels[role] || role;
  };

  return (
    <div className="profile-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-avatar-section">
            <div className="profile-avatar" onClick={() => fileInputRef.current?.click()}>
              {profileImage ? (
                <img src={profileImage} alt="Profile" className="avatar-image" />
              ) : (
                <div className="avatar-placeholder">
                  <User size={60} />
                </div>
              )}
              <div className="avatar-overlay">
                <Camera size={24} />
                <span>Changer</span>
              </div>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleProfileImageChange}
              style={{ display: 'none' }}
            />
          </div>
          <h1>👤 Mon Profil</h1>
          <p>Informations personnelles et code QR</p>
          <button className="btn-edit-profile" onClick={() => setShowEditModal(true)}>
            <Edit size={18} />
            Modifier le Profil
          </button>
        </div>

      <div className="profile-content">
        {/* Section Informations */}
        <div className="profile-section info-section">
          <h2>📋 Informations Personnelles</h2>
          
          <div className="info-grid">
            <div className="info-item">
              <div className="info-icon">
                <User size={20} />
              </div>
              <div className="info-text">
                <label>Nom d'utilisateur</label>
                <p>{user?.username}</p>
              </div>
            </div>

            <div className="info-item">
              <div className="info-icon">
                <Mail size={20} />
              </div>
              <div className="info-text">
                <label>Email</label>
                <p>{user?.email}</p>
              </div>
            </div>

            <div className="info-item">
              <div className="info-icon">
                <User size={20} />
              </div>
              <div className="info-text">
                <label>Nom Complet</label>
                <p>{user?.full_name}</p>
              </div>
            </div>

            <div className="info-item">
              <div className="info-icon">
                <Shield size={20} />
              </div>
              <div className="info-text">
                <label>Rôle</label>
                <p style={{ color: getRoleColor(user?.role) }}>
                  {getRoleLabel(user?.role)}
                </p>
              </div>
            </div>

            <div className="info-item">
              <div className="info-icon">
                <Calendar size={20} />
              </div>
              <div className="info-text">
                <label>Date de Création</label>
                <p>{new Date(user?.created_at).toLocaleDateString('fr-FR')}</p>
              </div>
            </div>

            <div className="info-item">
              <div className="info-icon">
                <QrCode size={20} />
              </div>
              <div className="info-text">
                <label>Code QR</label>
                <p>{user?.qr_code}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Section QR Code */}
        <div className="profile-section qr-section">
          <h2>📱 Mon Code QR</h2>
          <p className="qr-description">
            Partagez ce code QR pour que d'autres puissent vous identifier rapidement
          </p>

          <div className="qr-display">
            {user?.qr_code ? (
              qrImage ? (
                <div className="qr-card-modern">
                  {/* Phone Frame with QR Code */}
                  <div className="qr-phone-frame">
                    <div className="phone-notch"></div>
                    <div className="phone-screen">
                      <img src={qrImage} alt="Mon QR Code" className="qr-image-modern" onError={(e) => {
                        console.log('❌ Erreur chargement image QR');
                        e.target.src = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${user?.qr_code}`;
                      }} />
                    </div>
                  </div>
                  
                  {/* QR Info */}
                  <div className="qr-info-modern">
                    <h2 className="scan-me-title">scan<br/>ME!</h2>
                    <div className="qr-user-info">
                      <p className="user-name-qr">{user?.full_name}</p>
                      <p className="qr-code-label">Code: <span className="qr-code-value">{user?.qr_code}</span></p>
                      <p className="qr-scanner-link">Scanner sur:<br/>
                        <a href={`http://localhost:3000/qr-scanner?code=${user?.qr_code}`} target="_blank" rel="noopener noreferrer">
                          localhost:3000/qr-scanner
                        </a>
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="qr-loading">
                  <div className="spinner"></div>
                  <p>Chargement du QR Code...</p>
                </div>
              )
            ) : (
              <div className="qr-error">
                <QrCode size={60} />
                <p>❌ Aucun QR Code disponible</p>
                <small>Contactez un administrateur pour générer votre QR Code</small>
              </div>
            )}
          </div>

          <div className="qr-actions">
            <button className="btn-action btn-download" onClick={downloadQR}>
              <Download size={18} />
              Télécharger QR
            </button>
            <button 
              className="btn-action btn-copy" 
              onClick={copyQRCode}
              style={{ backgroundColor: copied ? '#43e97b' : '#667eea' }}
            >
              <Copy size={18} />
              {copied ? 'Copié!' : 'Copier Code'}
            </button>
            <button className="btn-action btn-test" onClick={testScanner}>
              <QrCode size={18} />
              Tester Scanner
            </button>
            <button className="btn-action btn-camera" onClick={startCameraScanner}>
              <Camera size={18} />
              Scanner Caméra
            </button>
          </div>

          <div className="qr-info">
            <h3>💡 Comment utiliser votre QR Code?</h3>
            <ul>
              <li>✅ Partagez votre QR code avec vos collègues</li>
              <li>✅ Ils peuvent vous scanner pour voir vos informations</li>
              <li>✅ Allez à <strong>http://localhost:3000/qr-scanner</strong></li>
              <li>✅ Entrez votre code QR: <strong>{user?.qr_code}</strong></li>
              <li>✅ Cliquez sur "Rechercher"</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Modal d'édition du profil */}
      {showEditModal && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>✏️ Modifier le Profil</h2>
              <button className="btn-close" onClick={() => setShowEditModal(false)}>
                <X size={24} />
              </button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label>Nom Complet</label>
                <input
                  type="text"
                  value={editData.full_name}
                  onChange={(e) => setEditData({...editData, full_name: e.target.value})}
                  placeholder="Votre nom complet"
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={editData.email}
                  onChange={(e) => setEditData({...editData, email: e.target.value})}
                  placeholder="votre.email@exemple.com"
                />
              </div>
              <div className="form-group">
                <label>Nom d'utilisateur</label>
                <input
                  type="text"
                  value={user?.username}
                  disabled
                  className="input-disabled"
                />
                <small>Le nom d'utilisateur ne peut pas être modifié</small>
              </div>
              <div className="form-group">
                <label>Rôle</label>
                <input
                  type="text"
                  value={getRoleLabel(user?.role)}
                  disabled
                  className="input-disabled"
                />
                <small>Le rôle ne peut être modifié que par un administrateur</small>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn-cancel" onClick={() => setShowEditModal(false)}>
                Annuler
              </button>
              <button className="btn-save" onClick={handleSaveProfile}>
                <Save size={18} />
                Enregistrer
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal Scanner Caméra */}
      {showCameraScanner && (
        <div className="modal-overlay" onClick={stopCameraScanner}>
          <div className="modal-content camera-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📷 Scanner QR Code</h2>
              <button className="btn-close" onClick={stopCameraScanner}>
                <X size={24} />
              </button>
            </div>
            <div className="modal-body">
              <div className="camera-container">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  className="camera-video"
                />
                <div className="scan-overlay">
                  <div className="scan-frame"></div>
                  <p>Placez le QR code dans le cadre</p>
                </div>
              </div>
              <div className="camera-instructions">
                <p>💡 Positionnez le QR code devant la caméra</p>
                <p>📱 Assurez-vous que l'éclairage est suffisant</p>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn-cancel" onClick={stopCameraScanner}>
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}

export default Profile;
