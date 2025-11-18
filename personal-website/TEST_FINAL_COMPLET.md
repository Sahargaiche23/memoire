# 🚀 TEST FINAL COMPLET - Profil et Upload d'Image

## ✅ OBJECTIFS

Vérifier que:
1. ✅ Modification de profil (nom, email) → Enregistré en DB
2. ✅ Upload d'image de profil → Fichier sauvegardé + Chemin en DB
3. ✅ Frontend → Backend communication
4. ✅ Persistance des données après reconnexion

---

## 🔧 ÉTAPE 1: PRÉPARATION

### A. Vérifier la base de données

```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend

# Vérifier la structure
sqlite3 instance/patrimoine.db "PRAGMA table_info(users);"

# Vérifier les utilisateurs
sqlite3 instance/patrimoine.db "SELECT id, username, full_name, email, profile_image FROM users;"
```

### B. Installer les dépendances Python (si nécessaire)

```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend
source /home/sahar/Bureau/Stage/venv/bin/activate
pip install Pillow requests
```

---

## 🚀 ÉTAPE 2: DÉMARRER LES SERVEURS

### Terminal 1 - Backend

```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend
source /home/sahar/Bureau/Stage/venv/bin/activate
python3 app.py
```

**Vérifier:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Terminal 2 - Frontend

```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/frontend
npm start
```

**Vérifier:**
```
Compiled successfully!
webpack compiled with 0 errors
```

**Navigateur s'ouvre:** http://localhost:3000

---

## 🧪 ÉTAPE 3: TEST AUTOMATIQUE (BACKEND)

### Terminal 3 - Tests automatiques

```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend
source /home/sahar/Bureau/Stage/venv/bin/activate
python3 test_profile_complet.py
```

**Résultats attendus:**
```
🧪 TEST COMPLET - PROFIL ET UPLOAD D'IMAGE
======================================================================

📝 TEST 1: CONNEXION
----------------------------------------------------------------------
✅ Connexion réussie!
   User ID: 7
   Username: sahar
   ...

📝 TEST 2: MODIFICATION DU PROFIL
----------------------------------------------------------------------
✅ Modification réussie!
   Nouveau nom: Test User 1763...
   Nouvel email: test1763...@example.com
✅ Données vérifiées en base de données!

📝 TEST 3: UPLOAD D'IMAGE DE PROFIL
----------------------------------------------------------------------
✅ Upload réussi!
   Fichier: profile_7_1763...png
   URL: /api/uploads/profile_7_1763...png
✅ Chemin sauvegardé en base de données!
✅ Fichier physique existe!

📝 TEST 4: VÉRIFICATION FINALE
----------------------------------------------------------------------
✅ Reconnexion réussie!
✅ Le nom a été persisté!
✅ L'email a été persisté!
✅ L'image a été persistée!

✅ Tests terminés!
```

---

## 🌐 ÉTAPE 4: TEST MANUEL (FRONTEND)

### A. Connexion

1. Allez à **http://localhost:3000**
2. **Connectez-vous:**
   - Username: `sahar`
   - Password: `test123`

### B. Vérifier le profil actuel

1. Cliquez sur **Profile** dans le menu
2. **Notez les données actuelles:**
   - Nom complet: _____________
   - Email: _____________
   - Image de profil: _____________

### C. Test modification de profil

1. Cliquez **"✏️ Modifier le Profil"**
2. **Changez:**
   - Nom complet: `Sahar Gaiche Final Test`
   - Email: `sahar.final@test.com`
3. Cliquez **"💾 Enregistrer"**

**Vérifications:**
- [ ] Alert de confirmation s'affiche
- [ ] Message: "✅ Profil mis à jour avec succès!"
- [ ] Page se recharge automatiquement
- [ ] Nouveau nom affiché: "Sahar Gaiche Final Test"
- [ ] Nouvel email affiché: "sahar.final@test.com"

**Console navigateur (F12):**
```
💾 Fonction handleSaveProfile appelée
Données à sauvegarder: {full_name: "Sahar Gaiche Final Test", ...}
✅ Mise à jour réussie: {...}
```

**Terminal backend:**
```
✅ Utilisateur sahar mis à jour: Sahar Gaiche Final Test / sahar.final@test.com
127.0.0.1 - - [XX:XX:XX] "PUT /api/users/7 HTTP/1.1" 200 -
```

### D. Test upload d'image

1. Dans la page **Profile**
2. **Cliquez sur l'avatar** (cercle avec icône utilisateur)
3. **Sélectionnez une image:**
   - Format: PNG, JPG, JPEG ou GIF
   - Taille max: 5MB
4. Attendez l'upload

**Vérifications:**
- [ ] Alert de confirmation s'affiche
- [ ] Message: "✅ Photo de profil uploadée et sauvegardée!"
- [ ] Page se recharge automatiquement
- [ ] Votre image s'affiche dans l'avatar
- [ ] L'image reste après rafraîchissement (Ctrl+R)

**Console navigateur (F12):**
```
📸 Fonction handleProfileImageChange appelée
Fichier: monimage.jpg Size: 45678 bytes
📤 Upload vers backend avec sauvegarde...
✅ Upload réussi: {filename: "profile_7_1763...jpg", ...}
```

**Terminal backend:**
```
✅ Image de profil uploadée pour sahar: profile_7_1763...jpg
127.0.0.1 - - [XX:XX:XX] "POST /api/users/7/profile-image HTTP/1.1" 200 -
```

### E. Test de persistance

1. **Déconnectez-vous** (bouton déconnexion)
2. **Fermez le navigateur complètement**
3. **Rouvrez** http://localhost:3000
4. **Reconnectez-vous:** `sahar` / `test123`
5. **Allez à Profile**

**Vérifications:**
- [ ] Nom affiché: "Sahar Gaiche Final Test" ✅
- [ ] Email affiché: "sahar.final@test.com" ✅
- [ ] Image de profil affichée ✅
- [ ] QR Code affiché ✅

**TOUT EST PERSISTÉ!** 🎉

---

## 🔍 ÉTAPE 5: VÉRIFICATION EN BASE DE DONNÉES

```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend

# Vérifier les données de l'utilisateur
sqlite3 instance/patrimoine.db "SELECT id, username, full_name, email, profile_image FROM users WHERE username='sahar';"
```

**Résultat attendu:**
```
7|sahar|Sahar Gaiche Final Test|sahar.final@test.com|profile_7_1763125XXX.jpg
```

### Vérifier le fichier image

```bash
ls -lh uploads/profile_7_*
```

**Résultat attendu:**
```
-rw-r--r-- 1 sahar sahar 45K Nov 17 13:XX uploads/profile_7_1763125XXX.jpg
```

### Vérifier via API

```bash
# Obtenir un token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "sahar", "password": "test123"}' | python3 -m json.tool
```

**Vérifier la réponse:**
```json
{
  "user": {
    "id": 7,
    "username": "sahar",
    "full_name": "Sahar Gaiche Final Test",
    "email": "sahar.final@test.com",
    "profile_image": "profile_7_1763125XXX.jpg",
    "qr_code": "GYAOGLGV",
    ...
  }
}
```

---

## 📊 CHECKLIST FINALE

### Backend:
- [ ] Serveur Flask démarre sans erreur
- [ ] Port 5000 actif
- [ ] Logs de requêtes visibles
- [ ] Colonne `profile_image` existe en DB
- [ ] Endpoint PUT `/api/users/:id` fonctionne
- [ ] Endpoint POST `/api/users/:id/profile-image` fonctionne
- [ ] Fichiers sauvegardés dans `/uploads/`

### Frontend:
- [ ] Serveur React démarre sans erreur
- [ ] Port 3000 actif
- [ ] Compilation sans warnings critiques
- [ ] Modal de modification s'ouvre
- [ ] Sélecteur d'image s'ouvre
- [ ] Requêtes vers localhost:5000 (PAS 3000!)
- [ ] Tokens JWT envoyés dans les headers

### Communication Frontend ↔ Backend:
- [ ] Requête PUT vers `http://localhost:5000/api/users/:id`
- [ ] Requête POST vers `http://localhost:5000/api/users/:id/profile-image`
- [ ] Headers Authorization avec Bearer token
- [ ] Réponses 200 OK
- [ ] Pas d'erreurs CORS

### Persistance:
- [ ] Données modifiées enregistrées en DB
- [ ] Image uploadée sauvegardée dans `/uploads/`
- [ ] Chemin image enregistré en DB
- [ ] Données affichées après reconnexion
- [ ] Image affichée après reconnexion

---

## ⚠️ DÉPANNAGE

### Problème: "Modification ne s'enregistre pas"

**Solution:**
1. Vérifier console navigateur (F12) pour erreurs
2. Vérifier terminal backend pour logs
3. Effacer cache navigateur: Ctrl+Shift+Delete
4. Déconnexion/Reconnexion

### Problème: "Image ne s'affiche pas"

**Solution:**
1. Vérifier que le fichier existe: `ls uploads/profile_*`
2. Vérifier la DB: `SELECT profile_image FROM users WHERE id=7;`
3. Vérifier l'URL: http://localhost:5000/api/uploads/profile_7_XXX.jpg
4. Rafraîchir avec Ctrl+F5

### Problème: "Erreur CORS"

**Solution:**
1. Vérifier que Flask-CORS est installé
2. Redémarrer le backend
3. Vérifier que les requêtes vont bien à localhost:5000

### Problème: "Token manquant"

**Solution:**
1. Déconnexion complète
2. Effacer localStorage: F12 → Application → Storage → Clear
3. Reconnexion

---

## ✅ RÉSULTAT ATTENDU

**SI TOUT FONCTIONNE:**
- ✅ Modification de profil → Enregistrée en DB
- ✅ Upload d'image → Fichier dans /uploads/ + chemin en DB
- ✅ Frontend → Backend communication parfaite
- ✅ Persistance totale après reconnexion
- ✅ Console backend affiche les logs de succès
- ✅ Console frontend ne montre pas d'erreurs

**SYSTÈME 100% FONCTIONNEL!** 🚀
