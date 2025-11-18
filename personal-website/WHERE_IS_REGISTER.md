# 🔐 Où Trouver le Register (Enregistrement)?

## 📍 Localisation du Register

### 1. Dans l'Interface Web (Frontend)

#### Pour Admin - Créer un Nouvel Utilisateur

1. **Connectez-vous** avec admin/admin123
2. **Cliquez sur "Utilisateurs"** dans la navigation
3. **Cliquez sur "+ Ajouter un utilisateur"**
4. **Remplissez le formulaire:**
   - Nom d'utilisateur
   - Email
   - Mot de passe
   - Nom complet
   - Rôle (5 options)
5. **Cliquez sur "Créer"**

✅ L'utilisateur est créé et peut se connecter!

---

### 2. Dans l'API Backend

#### Endpoint: `POST /api/auth/register`

**URL:**
```
http://localhost:5000/api/auth/register
```

**Méthode:** POST

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "username": "ali_ben",
  "email": "ali@municipality.tn",
  "password": "SecurePass2024!",
  "full_name": "Ali Ben Ahmed",
  "role": "responsable_patrimoine"
}
```

**Rôles Disponibles:**
- `admin` - Administrateur
- `responsable_patrimoine` - Responsable Patrimoine
- `responsable_service` - Responsable Service
- `agent_maintenance` - Agent Maintenance
- `auditeur` - Auditeur

**Réponse Succès (201):**
```json
{
  "message": "Utilisateur créé avec succès",
  "user": {
    "id": 6,
    "username": "ali_ben",
    "email": "ali@municipality.tn",
    "role": "responsable_patrimoine",
    "full_name": "Ali Ben Ahmed"
  }
}
```

**Réponse Erreur (400):**
```json
{
  "error": "Nom d'utilisateur existe déjà"
}
```

---

## 🧪 Tester avec Curl

### Créer un Utilisateur

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ali_ben",
    "email": "ali@municipality.tn",
    "password": "SecurePass2024!",
    "full_name": "Ali Ben Ahmed",
    "role": "responsable_patrimoine"
  }'
```

### Réponse Attendue

```json
{
  "message": "Utilisateur créé avec succès",
  "user": {
    "id": 6,
    "username": "ali_ben",
    "email": "ali@municipality.tn",
    "role": "responsable_patrimoine",
    "full_name": "Ali Ben Ahmed"
  }
}
```

---

## 🧪 Tester avec Postman

### Étapes

1. **Ouvrez Postman**
2. **Créez une nouvelle requête**
3. **Sélectionnez POST**
4. **URL:** `http://localhost:5000/api/auth/register`
5. **Onglet Headers:**
   - Key: `Content-Type`
   - Value: `application/json`
6. **Onglet Body:**
   - Sélectionnez `raw`
   - Sélectionnez `JSON`
   - Collez:
   ```json
   {
     "username": "ali_ben",
     "email": "ali@municipality.tn",
     "password": "SecurePass2024!",
     "full_name": "Ali Ben Ahmed",
     "role": "responsable_patrimoine"
   }
   ```
7. **Cliquez sur Send**

---

## 📁 Fichiers Concernés

### Backend
- **`backend/app.py`** - Endpoint `/api/auth/register` (ligne 92-139)
- **`backend/init_db.py`** - Initialisation des utilisateurs de démo

### Frontend
- **`frontend/src/pages/Users.js`** - Page de gestion des utilisateurs
- **`frontend/src/utils/roleAccess.js`** - Gestion des rôles

---

## 🔄 Flux de Création d'Utilisateur

### Via Interface Web

```
Admin Login
    ↓
Navigation → Utilisateurs
    ↓
Cliquer "+ Ajouter un utilisateur"
    ↓
Remplir le formulaire
    ↓
Cliquer "Créer"
    ↓
POST /api/auth/register
    ↓
Validation Backend
    ↓
Création en BD
    ↓
Message de Succès
    ↓
Utilisateur peut se connecter
```

### Via API

```
POST /api/auth/register
    ↓
Validation des données
    ↓
Vérification des doublons
    ↓
Hachage du mot de passe
    ↓
Création en BD
    ↓
Réponse JSON
```

---

## ✅ Validation des Données

### Champs Obligatoires
- ✅ `username` - Unique, min 3 caractères
- ✅ `email` - Unique, format email valide
- ✅ `password` - Min 6 caractères
- ✅ `role` - Parmi les 5 rôles valides

### Champs Optionnels
- ⚪ `full_name` - Nom complet de l'utilisateur

### Validation Backend
```python
# Vérifier que les champs obligatoires sont présents
required_fields = ['username', 'email', 'password', 'role']

# Vérifier que l'utilisateur n'existe pas
if User.query.filter_by(username=data['username']).first():
    return error

# Vérifier que l'email n'existe pas
if User.query.filter_by(email=data['email']).first():
    return error

# Valider le rôle
valid_roles = ['admin', 'responsable_patrimoine', ...]
if data['role'] not in valid_roles:
    return error
```

---

## 🔐 Sécurité

### Mot de Passe
- ✅ Hachage avec Werkzeug
- ✅ Jamais stocké en clair
- ✅ Min 6 caractères recommandé

### Validation
- ✅ Vérification des doublons
- ✅ Validation du rôle
- ✅ Validation des champs obligatoires

### Contrôle d'Accès
- ✅ Seul l'admin peut créer des utilisateurs
- ✅ JWT requis pour l'endpoint

---

## 📊 Exemple: Créer 3 Utilisateurs

### Utilisateur 1: Responsable Patrimoine

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fatima_ali",
    "email": "fatima@municipality.tn",
    "password": "FatimaPass2024!",
    "full_name": "Fatima Ali Mohamed",
    "role": "responsable_patrimoine"
  }'
```

### Utilisateur 2: Agent Maintenance

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hassan_tech",
    "email": "hassan@municipality.tn",
    "password": "HassanTech2024!",
    "full_name": "Hassan Khaled",
    "role": "agent_maintenance"
  }'
```

### Utilisateur 3: Auditeur

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "zahra_audit",
    "email": "zahra@municipality.tn",
    "password": "ZahraAudit2024!",
    "full_name": "Zahra Ben Salah",
    "role": "auditeur"
  }'
```

---

## 🎯 Cas d'Usage

### Cas 1: Admin Crée un Nouvel Agent

1. Admin se connecte
2. Va à Utilisateurs
3. Clique "+ Ajouter un utilisateur"
4. Remplit le formulaire avec:
   - Username: `ahmed_agent`
   - Email: `ahmed@municipality.tn`
   - Password: `AhmedAgent2024!`
   - Full Name: `Ahmed Khaled`
   - Role: `agent_maintenance`
5. Clique "Créer"
6. Ahmed peut maintenant se connecter

### Cas 2: API Crée un Utilisateur

```bash
# Créer un utilisateur via API
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "omar_service",
    "email": "omar@municipality.tn",
    "password": "OmarService2024!",
    "full_name": "Omar Saïd",
    "role": "responsable_service"
  }'

# Omar peut maintenant se connecter
```

---

## 📝 Résumé

| Aspect | Détails |
|--------|---------|
| **Où** | Interface Web → Utilisateurs → + Ajouter |
| **Ou** | API → POST /api/auth/register |
| **Qui** | Admin uniquement |
| **Quoi** | Créer de nouveaux utilisateurs |
| **Rôles** | 5 rôles disponibles |
| **Validation** | Complète (backend + frontend) |

---

**Dernière mise à jour**: Novembre 2024
