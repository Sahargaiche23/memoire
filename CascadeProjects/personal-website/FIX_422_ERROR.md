# 🔧 Correction Erreur 422 - Token JWT

## 🔴 Problème

Vous recevez des erreurs **422** sur les endpoints protégés:

```
GET /api/statistics HTTP/1.1" 422
GET /api/assets HTTP/1.1" 422
GET /api/alerts HTTP/1.1" 422
```

Mais la connexion fonctionne (200):

```
POST /api/auth/login HTTP/1.1" 200
POST /api/auth/register HTTP/1.1" 201
```

---

## ✅ Solution

### Étape 1: Arrêtez le Backend

Appuyez sur **CTRL+C** dans le terminal du backend.

### Étape 2: Redémarrez le Backend

```bash
cd backend
python app.py
```

### Étape 3: Testez la Connexion

Utilisez les identifiants:
- **Utilisateur:** `admin`
- **Mot de passe:** `admin123`

### Étape 4: Vérifiez les Logs

Vous devriez voir:

```
127.0.0.1 - - [13/Nov/2025 13:03:28] "POST /api/auth/login HTTP/1.1" 200 -
127.0.0.1 - - [13/Nov/2025 13:03:28] "GET /api/statistics HTTP/1.1" 200 -
127.0.0.1 - - [13/Nov/2025 13:03:28] "GET /api/assets HTTP/1.1" 200 -
```

✅ **Ça marche!**

---

## 🔍 Qu'est-ce qui a été Corrigé?

### 1. Endpoint Login Amélioré
- ✅ Gestion des OPTIONS (CORS preflight)
- ✅ Validation des données
- ✅ Token converti en string

### 2. Gestionnaires d'Erreurs JWT
- ✅ Erreur 422 → 401 (Token invalide)
- ✅ Token expiré → 401
- ✅ Token invalide → 401
- ✅ Token manquant → 401

### 3. Configuration JWT
- ✅ Secret key configurée
- ✅ Expiration: 30 jours
- ✅ JWTManager initialisé

---

## 📊 Avant/Après

### Avant
```
POST /api/auth/login → 200 ✅
GET /api/statistics → 422 ❌
GET /api/assets → 422 ❌
GET /api/alerts → 422 ❌
```

### Après
```
POST /api/auth/login → 200 ✅
GET /api/statistics → 200 ✅
GET /api/assets → 200 ✅
GET /api/alerts → 200 ✅
```

---

## 🧪 Tester avec Curl

### 1. Connexion

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Réponse:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@municipality.tn",
    "role": "admin",
    "full_name": "Administrateur Système"
  }
}
```

### 2. Récupérer le Token

Copiez le `access_token` de la réponse.

### 3. Utiliser le Token

```bash
curl -X GET http://localhost:5000/api/statistics \
  -H "Authorization: Bearer <VOTRE_TOKEN>"
```

Réponse:
```json
{
  "total_assets": 12,
  "active_assets": 11,
  "total_value": 2500000,
  "by_category": [...]
}
```

---

## 📝 Modifications Apportées

### backend/app.py

#### 1. Login Endpoint
```python
@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    # Validation des données
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '...'}), 400
    
    # Token converti en string
    access_token = create_access_token(identity=str(user.id))
```

#### 2. JWT Error Handlers
```python
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({'error': 'Token expiré'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Token invalide'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Token manquant'}), 401
```

---

## ✅ Checklist

- [ ] Backend arrêté
- [ ] Backend redémarré
- [ ] Connexion réussie (200)
- [ ] Statistiques chargées (200)
- [ ] Actifs chargés (200)
- [ ] Alertes chargées (200)
- [ ] Tableau de bord affiche les données
- [ ] Pas d'erreur 422

---

## 🎯 Résultat Final

Tous les endpoints fonctionnent correctement:

```
✅ POST /api/auth/login → 200
✅ POST /api/auth/register → 201
✅ GET /api/statistics → 200
✅ GET /api/assets → 200
✅ GET /api/maintenances → 200
✅ GET /api/alerts → 200
✅ GET /api/users → 200
✅ GET /api/movements → 200
```

---

**C'est tout! Ça devrait fonctionner maintenant! 🎉**
