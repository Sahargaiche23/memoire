# 🗑️ TEST - Suppression d'Utilisateur

## 🎯 OBJECTIF

Vérifier que la suppression d'utilisateur fonctionne correctement.

---

## ⚙️ PRÉPARATION

### 1. Connexion Admin

```
Username: admin
Password: test123
```

**Si erreur 401:**
```bash
cd backend
python3 -c "
import sys; sys.path.insert(0, '.')
from app import app, db, User
from werkzeug.security import generate_password_hash
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.password_hash = generate_password_hash('test123')
        db.session.commit()
        print('✅ Mot de passe admin: test123')
"
```

### 2. Créer un utilisateur de test

**Option A: Via l'interface**
- Menu → Utilisateurs
- "+ Ajouter un utilisateur"
- Username: `testdelete`
- Email: `testdelete@test.com`
- Password: `test123`
- Nom: `Test Delete`
- Rôle: user
- Créer

**Option B: Via script**
```bash
cd backend
python3 -c "
import requests
response = requests.post('http://localhost:5000/api/auth/register', json={
    'username': 'testdelete',
    'email': 'testdelete@test.com',
    'password': 'test123',
    'full_name': 'Test Delete',
    'role': 'user'
})
print(response.status_code, response.json())
"
```

---

## 🧪 TEST DE SUPPRESSION

### Étape 1: Vérifier l'utilisateur existe

```bash
cd backend
sqlite3 instance/patrimoine.db "SELECT id, username, email FROM users WHERE username='testdelete';"
```

**Résultat attendu:**
```
9|testdelete|testdelete@test.com
```

### Étape 2: Ouvrir la console (F12)

- Appuyez sur **F12**
- Allez à l'onglet **Console**

### Étape 3: Supprimer via l'interface

1. **Utilisateurs** → Trouver "testdelete"
2. **Cliquez l'icône 🗑️** (poubelle rouge)
3. **Confirmez** dans la popup

### Étape 4: Vérifications

**Console (F12):**
```
🗑️ Suppression utilisateur ID: 9
✅ Réponse suppression: {message: "Utilisateur supprimé"}
```

**Alert popup:**
```
✅ Utilisateur supprimé avec succès!
```

**Terminal backend:**
```
127.0.0.1 - - [XX:XX:XX] "DELETE /api/users/9 HTTP/1.1" 200 -
```

**Tableau:**
- L'utilisateur "testdelete" disparaît

### Étape 5: Vérifier en base de données

```bash
sqlite3 instance/patrimoine.db "SELECT id, username FROM users WHERE username='testdelete';"
```

**Résultat attendu:**
```
(rien - l'utilisateur a été supprimé)
```

---

## ❌ PROBLÈMES POSSIBLES

### Problème 1: Bouton ne fait rien

**Symptômes:**
- Clic sur 🗑️ → Rien ne se passe
- Pas de popup de confirmation

**Causes possibles:**
1. JavaScript erreur
2. Event handler non attaché

**Solution:**
1. Vérifier console (F12) pour erreurs
2. Rafraîchir la page (Ctrl+F5)
3. Vérifier que Users.js est bien chargé

### Problème 2: Erreur 401 Unauthorized

**Symptômes:**
- Console: "❌ Erreur suppression: 401"
- Alert: "❌ Token manquant"

**Solution:**
- Déconnexion
- Reconnexion admin
- Réessayer

### Problème 3: Erreur 403 Forbidden

**Symptômes:**
- Console: "❌ Erreur suppression: 403"
- Alert: "❌ Permissions insuffisantes"

**Solution:**
- Vérifier que vous êtes connecté en tant qu'admin
- Vérifier le rôle: `admin` ou `responsable_patrimoine`

### Problème 4: Erreur 500 Server Error

**Symptômes:**
- Console: "❌ Erreur suppression: 500"
- Terminal backend: Erreur SQL

**Causes possibles:**
- Contrainte de clé étrangère
- Utilisateur lié à d'autres données

**Terminal backend montre:**
```
❌ Erreur lors de la suppression: FOREIGN KEY constraint failed
```

**Solution:**
Le backend supprime déjà:
- Messages envoyés
- Messages reçus
- Chat messages

Si autre contrainte, vérifier la base de données.

### Problème 5: Utilisateur réapparaît

**Symptômes:**
- Suppression semble fonctionner
- Rafraîchissement → Utilisateur revient

**Cause:**
- Suppression non committée en DB

**Solution:**
```bash
# Vérifier la DB
sqlite3 instance/patrimoine.db "SELECT username FROM users;"
```

---

## 🔍 TEST DÉTAILLÉ

### Test complet avec logs:

1. **Connexion admin**
   - Ouvrir F12 (console)
   - Se connecter

2. **Créer utilisateur**
   ```javascript
   // Dans la console:
   const token = localStorage.getItem('token');
   fetch('http://localhost:5000/api/auth/register', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({
       username: 'testdelete2',
       email: 'testdelete2@test.com',
       password: 'test123',
       full_name: 'Test Delete 2',
       role: 'user'
     })
   }).then(r => r.json()).then(d => console.log('✅ Créé:', d));
   ```

3. **Supprimer utilisateur**
   - Rafraîchir la page
   - Trouver "testdelete2"
   - Cliquer 🗑️
   - Confirmer

4. **Vérifier logs**
   ```javascript
   // Console devrait montrer:
   🗑️ Suppression utilisateur ID: 10
   ✅ Réponse suppression: {message: "Utilisateur supprimé"}
   ```

---

## 🎯 CHECKLIST

### Avant suppression:
- [ ] Admin connecté
- [ ] Page Utilisateurs ouverte
- [ ] Console F12 ouverte
- [ ] Utilisateur de test créé
- [ ] Utilisateur visible dans le tableau

### Pendant suppression:
- [ ] Clic sur 🗑️
- [ ] Popup de confirmation s'affiche
- [ ] Confirmation cliquée

### Après suppression:
- [ ] Console montre "🗑️ Suppression..."
- [ ] Console montre "✅ Réponse suppression"
- [ ] Alert "✅ Utilisateur supprimé"
- [ ] Terminal backend: 200
- [ ] Utilisateur disparu du tableau
- [ ] DB: Utilisateur supprimé

---

## 📝 VÉRIFICATION BACKEND

### Tester directement l'API:

```bash
# 1. Se connecter
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "test123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"

# 2. Créer utilisateur
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testapi",
    "email": "testapi@test.com",
    "password": "test123",
    "full_name": "Test API",
    "role": "user"
  }'

# 3. Trouver l'ID
ID=$(sqlite3 instance/patrimoine.db "SELECT id FROM users WHERE username='testapi';")
echo "ID: $ID"

# 4. Supprimer
curl -X DELETE "http://localhost:5000/api/users/$ID" \
  -H "Authorization: Bearer $TOKEN"

# 5. Vérifier
sqlite3 instance/patrimoine.db "SELECT username FROM users WHERE username='testapi';"
# Devrait être vide
```

---

## ✅ RÉSULTAT ATTENDU

**Si tout fonctionne:**
- ✅ Popup de confirmation
- ✅ Console: Logs de suppression
- ✅ Alert: Succès
- ✅ Tableau: Utilisateur disparu
- ✅ Backend: 200 OK
- ✅ DB: Utilisateur supprimé

**LA SUPPRESSION FONCTIONNE!** 🎉

---

## 🚨 SI ÇA NE FONCTIONNE TOUJOURS PAS

### Redémarrer complètement:

```bash
# Backend
Ctrl+C (arrêter)
python3 app.py

# Frontend
Ctrl+C (arrêter)
npm start
```

### Vider le cache:
- Ctrl+Shift+Delete
- Cocher "Cache" et "Cookies"
- Effacer

### Reconnexion:
- Déconnexion
- Reconnexion admin

---

**TESTEZ MAINTENANT ET VÉRIFIEZ LES LOGS!** 🔍
