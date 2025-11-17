# 🚀 NOUVELLES FONCTIONNALITÉS

## ✅ CORRECTIONS EFFECTUÉES

### 1. **Fix Erreur de Recherche**
**Problème:** `can't access property 'toLowerCase', asset.location is null`

**Correction:**
```javascript
// AVANT (❌)
asset.location.toLowerCase()

// MAINTENANT (✅)
(asset.location && asset.location.toLowerCase())
```

**Fichier modifié:** `frontend/src/pages/AssetSearch.js`

---

## 📋 FONCTIONNALITÉS À AJOUTER

### 2. **QR Code Automatique pour Actifs**

**Backend - Modifier l'endpoint de création d'actif:**

```python
# backend/app.py - Dans create_asset()

import qrcode
import random
import string

def generate_qr_code_for_asset(asset):
    """Génère un QR code unique pour un actif"""
    # Générer un code unique
    qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Créer le QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"ASSET_{asset.id}_{qr_code}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Sauvegarder l'image
    filename = f"qr_asset_{asset.id}_{qr_code}.png"
    filepath = os.path.join(QR_CODES_FOLDER, filename)
    img.save(filepath)
    
    return qr_code

# Dans create_asset():
@app.route('/api/assets', methods=['POST'])
@jwt_required()
def create_asset():
    data = request.get_json()
    
    new_asset = Asset(
        name=data['name'],
        category=data.get('category'),
        location=data.get('location'),
        current_value=data.get('current_value'),
        acquisition_date=datetime.strptime(data['acquisition_date'], '%Y-%m-%d').date(),
        status=data.get('status', 'actif'),
        description=data.get('description')
    )
    
    db.session.add(new_asset)
    db.session.flush()  # Pour obtenir l'ID
    
    # ✅ Générer le QR code automatiquement
    qr_code = generate_qr_code_for_asset(new_asset)
    new_asset.qr_code = qr_code
    
    db.session.commit()
    
    print(f"✅ Actif créé avec QR code: {qr_code}")
    
    return jsonify({
        'id': new_asset.id,
        'qr_code': qr_code,  # ← Retourner le QR code
        'message': 'Actif créé'
    }), 201
```

---

### 3. **QR Code Automatique pour Maintenances**

**Backend - Modifier l'endpoint de création de maintenance:**

```python
# backend/app.py

def generate_qr_code_for_maintenance(maintenance):
    """Génère un QR code unique pour une maintenance"""
    qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"MAINT_{maintenance.id}_{qr_code}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"qr_maintenance_{maintenance.id}_{qr_code}.png"
    filepath = os.path.join(QR_CODES_FOLDER, filename)
    img.save(filepath)
    
    return qr_code

# Dans create_maintenance():
@app.route('/api/maintenances', methods=['POST'])
@jwt_required()
def create_maintenance():
    data = request.get_json()
    
    maintenance = Maintenance(
        asset_id=data['asset_id'],
        maintenance_type=data['maintenance_type'],
        scheduled_date=datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date(),
        description=data.get('description', ''),
        cost=data.get('cost'),
        status=data.get('status', 'planifiée')
    )
    
    db.session.add(maintenance)
    db.session.flush()
    
    # ✅ Générer le QR code automatiquement
    qr_code = generate_qr_code_for_maintenance(maintenance)
    maintenance.qr_code = qr_code
    
    db.session.commit()
    
    print(f"✅ Maintenance créée avec QR code: {qr_code}")
    
    return jsonify({
        'id': maintenance.id,
        'qr_code': qr_code,
        'message': 'Maintenance créée'
    }), 201
```

---

### 4. **Ajouter Carte Interactive dans Recherche**

**Installation de Leaflet (carte):**
```bash
cd frontend
npm install react-leaflet leaflet
```

**Modification de AssetSearch.js:**

```javascript
// frontend/src/pages/AssetSearch.js

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Ajouter state pour la carte
const [showMap, setShowMap] = useState(false);
const [mapCenter, setMapCenter] = useState([36.8065, 10.1815]); // Tunis

// Fonction pour obtenir les coordonnées d'un actif
const getAssetCoordinates = (asset) => {
  // Si l'actif a des coordonnées GPS
  if (asset.latitude && asset.longitude) {
    return [asset.latitude, asset.longitude];
  }
  
  // Sinon, coordonnées par défaut basées sur la location
  const locations = {
    'centre-ville': [36.8065, 10.1815],
    'banlieue': [36.8500, 10.2000],
    // Ajouter plus de locations
  };
  
  return locations[asset.location] || [36.8065, 10.1815];
};

// Dans le render, ajouter le bouton et la carte
return (
  <div className="asset-search-page">
    <Navbar user={user} onLogout={onLogout} />
    
    <div className="search-container">
      <h1>🔍 Recherche d'Actifs</h1>
      
      {/* Bouton pour afficher/masquer la carte */}
      <button 
        className="btn btn-primary" 
        onClick={() => setShowMap(!showMap)}
      >
        {showMap ? '📋 Liste' : '🗺️ Carte'}
      </button>
      
      {/* Carte interactive */}
      {showMap && (
        <div className="map-container" style={{ height: '500px', marginTop: '20px' }}>
          <MapContainer 
            center={mapCenter} 
            zoom={13} 
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; OpenStreetMap contributors'
            />
            
            {/* Marqueurs pour chaque actif */}
            {filteredAssets.map(asset => {
              const coords = getAssetCoordinates(asset);
              return (
                <Marker key={asset.id} position={coords}>
                  <Popup>
                    <strong>{asset.name}</strong><br/>
                    Catégorie: {asset.category}<br/>
                    Localisation: {asset.location}<br/>
                    Statut: {asset.status}
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>
      )}
      
      {/* Liste des actifs (existant) */}
      {!showMap && (
        <div className="assets-grid">
          {/* Code existant */}
        </div>
      )}
    </div>
  </div>
);
```

---

## 🗄️ MODIFICATIONS BASE DE DONNÉES

### Ajouter colonnes pour coordonnées GPS et QR codes:

```sql
-- Pour les actifs
ALTER TABLE assets ADD COLUMN latitude FLOAT;
ALTER TABLE assets ADD COLUMN longitude FLOAT;
ALTER TABLE assets ADD COLUMN qr_code VARCHAR(20);

-- Pour les maintenances
ALTER TABLE maintenances ADD COLUMN qr_code VARCHAR(20);
```

**Script Python de migration:**

```python
# backend/migrate_add_qr_and_gps.py

import sys
sys.path.insert(0, '.')

from app import app, db

with app.app_context():
    # Ajouter les colonnes
    db.session.execute('ALTER TABLE assets ADD COLUMN IF NOT EXISTS latitude FLOAT')
    db.session.execute('ALTER TABLE assets ADD COLUMN IF NOT EXISTS longitude FLOAT')
    db.session.execute('ALTER TABLE assets ADD COLUMN IF NOT EXISTS qr_code VARCHAR(20)')
    db.session.execute('ALTER TABLE maintenances ADD COLUMN IF NOT EXISTS qr_code VARCHAR(20)')
    
    db.session.commit()
    print("✅ Colonnes ajoutées!")
```

---

## 📦 DÉPENDANCES À INSTALLER

### Backend:
```bash
cd backend
pip install qrcode Pillow
```

### Frontend:
```bash
cd frontend
npm install react-leaflet leaflet
```

---

## 🧪 TESTS

### Test 1: QR Code Actif
1. Créer un nouvel actif
2. Vérifier que le QR code est généré
3. Vérifier l'image dans `backend/qr_codes/`

### Test 2: QR Code Maintenance
1. Créer une nouvelle maintenance
2. Vérifier que le QR code est généré
3. Vérifier l'image dans `backend/qr_codes/`

### Test 3: Carte
1. Aller sur la page Recherche
2. Cliquer sur "🗺️ Carte"
3. Vérifier que les actifs s'affichent sur la carte

---

## ✅ RÉSUMÉ

**FAIT:**
- ✅ Fix erreur recherche (asset.location null)

**À FAIRE:**
- [ ] Ajouter génération QR pour actifs
- [ ] Ajouter génération QR pour maintenances
- [ ] Installer react-leaflet
- [ ] Ajouter carte interactive
- [ ] Migrer la base de données

**TEMPS ESTIMÉ:** 2-3 heures
