import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Search, MapPin, DollarSign, Calendar, Filter, X, Map as MapIcon, List } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import './AssetSearch.css';

// Fix pour les icônes Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

// Composant pour centrer la carte sur un actif
function MapFocusController({ center, zoom }) {
  const map = useMap();
  
  useEffect(() => {
    if (center && center.length === 2) {
      map.setView(center, zoom, {
        animate: true,
        duration: 1
      });
    }
  }, [center, zoom, map]);
  
  return null;
}

function AssetSearch({ user, onLogout }) {
  const [assets, setAssets] = useState([]);
  const [filteredAssets, setFilteredAssets] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showMap, setShowMap] = useState(false);
  const [mapCenter, setMapCenter] = useState([36.8065, 10.1815]); // Tunis - centre par défaut
  const [mapZoom, setMapZoom] = useState(12);
  const mapRef = useRef(null);
  const token = localStorage.getItem('token');

  const categories = ['all', 'bâtiment', 'véhicule', 'équipement', 'mobilier', 'terrain'];
  const statuses = ['all', 'actif', 'maintenance', 'hors_service', 'déclassé'];

  // Coordonnées GPS par défaut selon la localisation
  const getAssetCoordinates = (asset) => {
    // Coordonnées par défaut basées sur la location
    const locations = {
      'hammam-lif': [36.7300, 10.3400],
      'centre-ville': [36.8065, 10.1815],
      'banlieue': [36.8500, 10.2000],
      'nord': [36.8700, 10.1700],
      'sud': [36.7500, 10.2200],
      'default': [36.8065, 10.1815]
    };
    
    // Utiliser la location ou coordonnées par défaut
    const locationKey = asset.location ? asset.location.toLowerCase() : 'default';
    return locations[locationKey] || locations['default'];
  };

  useEffect(() => {
    fetchAssets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    filterAssets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [assets, searchTerm, selectedCategory, selectedStatus]);

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

  const filterAssets = () => {
    let filtered = assets;

    // Filtre par recherche
    if (searchTerm) {
      filtered = filtered.filter(asset =>
        (asset.name && asset.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (asset.location && asset.location.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (asset.description && asset.description.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filtre par catégorie
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(asset => asset.category === selectedCategory);
    }

    // Filtre par statut
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(asset => asset.status === selectedStatus);
    }

    setFilteredAssets(filtered);
  };

  const getCategoryColor = (category) => {
    const colors = {
      'bâtiment': '#667eea',
      'véhicule': '#764ba2',
      'équipement': '#f093fb',
      'mobilier': '#4facfe',
      'terrain': '#43e97b'
    };
    return colors[category] || '#667eea';
  };

  const getStatusBadge = (status) => {
    const badges = {
      'actif': { bg: '#43e97b', text: 'Actif' },
      'maintenance': { bg: '#f093fb', text: 'Maintenance' },
      'hors_service': { bg: '#ff6b6b', text: 'Hors Service' },
      'déclassé': { bg: '#999', text: 'Déclassé' }
    };
    return badges[status] || { bg: '#667eea', text: status };
  };

  // Fonction pour centrer la carte sur un actif
  const focusOnAsset = (asset) => {
    const coords = getAssetCoordinates(asset);
    setMapCenter(coords);
    setMapZoom(15); // Zoom plus proche
    setSelectedAsset(asset);
    
    // Basculer automatiquement vers la carte si on est en mode liste
    if (!showMap) {
      setShowMap(true);
    }
  };

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="asset-search-page">
      <Navbar user={user} onLogout={onLogout} />

      <div className="search-container">
        {/* Sidebar Filtres */}
        <div className="search-sidebar">
          <div className="sidebar-header">
            <Filter size={20} />
            <h2>Filtres</h2>
          </div>

          {/* Barre de recherche */}
          <div className="search-input-wrapper">
            <Search size={18} />
            <input
              type="text"
              placeholder="Rechercher..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <button onClick={() => setSearchTerm('')} className="clear-btn">
                <X size={16} />
              </button>
            )}
          </div>

          {/* Filtre Catégorie */}
          <div className="filter-group">
            <h3>Catégorie</h3>
            <div className="filter-options">
              {categories.map(cat => (
                <label key={cat} className="filter-option">
                  <input
                    type="radio"
                    name="category"
                    value={cat}
                    checked={selectedCategory === cat}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                  />
                  <span>
                    {cat === 'all' ? 'Tous' : cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Filtre Statut */}
          <div className="filter-group">
            <h3>Statut</h3>
            <div className="filter-options">
              {statuses.map(status => (
                <label key={status} className="filter-option">
                  <input
                    type="radio"
                    name="status"
                    value={status}
                    checked={selectedStatus === status}
                    onChange={(e) => setSelectedStatus(e.target.value)}
                  />
                  <span>
                    {status === 'all' ? 'Tous' : status.charAt(0).toUpperCase() + status.slice(1)}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Résultats */}
          <div className="results-count">
            <p>{filteredAssets.length} résultat(s)</p>
          </div>
        </div>

        {/* Contenu Principal */}
        <div className="search-main">
          {/* Bouton pour basculer entre Liste et Carte */}
          <div className="view-toggle">
            <button 
              className={`toggle-btn ${!showMap ? 'active' : ''}`}
              onClick={() => setShowMap(false)}
            >
              <List size={18} />
              <span>Liste</span>
            </button>
            <button 
              className={`toggle-btn ${showMap ? 'active' : ''}`}
              onClick={() => setShowMap(true)}
            >
              <MapIcon size={18} />
              <span>Carte</span>
            </button>
            <div className="results-count">
              {filteredAssets.length} actif{filteredAssets.length > 1 ? 's' : ''}
            </div>
          </div>

          {/* Carte Interactive */}
          {showMap && (
            <div className="map-container">
              <MapContainer 
                center={mapCenter} 
                zoom={mapZoom} 
                style={{ height: '600px', width: '100%', borderRadius: '12px' }}
                ref={mapRef}
              >
                <MapFocusController center={mapCenter} zoom={mapZoom} />
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                
                {filteredAssets.map(asset => {
                  const coords = getAssetCoordinates(asset);
                  return (
                    <Marker key={asset.id} position={coords}>
                      <Popup>
                        <div className="map-popup">
                          <h3>{asset.name}</h3>
                          <p><strong>Catégorie:</strong> {asset.category}</p>
                          <p><strong>Localisation:</strong> {asset.location}</p>
                          <p><strong>Statut:</strong> {asset.status}</p>
                          <p><strong>Valeur:</strong> {asset.current_value.toLocaleString()} DT</p>
                        </div>
                      </Popup>
                    </Marker>
                  );
                })}
              </MapContainer>
            </div>
          )}

          {/* Grille des actifs */}
          {!showMap && (
            <div className="assets-grid">
            {filteredAssets.length === 0 ? (
              <div className="no-results">
                <Search size={48} />
                <p>Aucun actif trouvé</p>
              </div>
            ) : (
              filteredAssets.map(asset => (
                <div
                  key={asset.id}
                  className={`asset-card ${selectedAsset?.id === asset.id ? 'active' : ''}`}
                  onClick={() => focusOnAsset(asset)}
                >
                  <div className="asset-card-header">
                    <div
                      className="category-badge"
                      style={{ backgroundColor: getCategoryColor(asset.category) }}
                    >
                      {asset.category.charAt(0).toUpperCase()}
                    </div>
                    <div
                      className="status-badge"
                      style={{ backgroundColor: getStatusBadge(asset.status).bg }}
                    >
                      {getStatusBadge(asset.status).text}
                    </div>
                  </div>

                  <h3>{asset.name}</h3>
                  <p className="category">{asset.category}</p>

                  <div className="asset-info">
                    <div className="info-item">
                      <MapPin size={14} />
                      <span>{asset.location}</span>
                    </div>
                    <div className="info-item">
                      <DollarSign size={14} />
                      <span>{asset.current_value.toLocaleString()} DT</span>
                    </div>
                    <div className="info-item">
                      <Calendar size={14} />
                      <span>{new Date(asset.acquisition_date).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <p className="description">{asset.description}</p>
                </div>
              ))
            )}
            </div>
          )}

          {/* Détails de l'actif sélectionné */}
          {selectedAsset && (
            <div className="asset-details">
              <div className="details-header">
                <h2>{selectedAsset.name}</h2>
                <button onClick={() => setSelectedAsset(null)} className="close-btn">
                  <X size={24} />
                </button>
              </div>

              {/* Bouton pour voir sur la carte */}
              <button 
                className="btn-view-on-map"
                onClick={() => focusOnAsset(selectedAsset)}
              >
                <MapPin size={18} />
                <span>Voir sur la carte</span>
              </button>

              <div className="details-content">
                <div className="detail-section">
                  <h3>📍 Localisation</h3>
                  <p>{selectedAsset.location}</p>
                </div>

                <div className="detail-section">
                  <h3>📋 Catégorie</h3>
                  <p>{selectedAsset.category}</p>
                </div>

                <div className="detail-section">
                  <h3>📊 Statut</h3>
                  <p>{getStatusBadge(selectedAsset.status).text}</p>
                </div>

                <div className="detail-section">
                  <h3>💰 Valeur</h3>
                  <div className="value-info">
                    <div>
                      <p className="label">Acquisition</p>
                      <p className="value">{selectedAsset.acquisition_value.toLocaleString()} DT</p>
                    </div>
                    <div>
                      <p className="label">Actuelle</p>
                      <p className="value">{selectedAsset.current_value.toLocaleString()} DT</p>
                    </div>
                  </div>
                </div>

                <div className="detail-section">
                  <h3>📅 Date d'Acquisition</h3>
                  <p>{new Date(selectedAsset.acquisition_date).toLocaleDateString()}</p>
                </div>

                <div className="detail-section">
                  <h3>📝 Description</h3>
                  <p>{selectedAsset.description}</p>
                </div>

                <div className="detail-section">
                  <h3>👤 Affecté à</h3>
                  <p>{selectedAsset.assigned_to}</p>
                </div>

                <div className="detail-section">
                  <h3>🔐 Code QR</h3>
                  <p className="qr-code">{selectedAsset.qr_code}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AssetSearch;
