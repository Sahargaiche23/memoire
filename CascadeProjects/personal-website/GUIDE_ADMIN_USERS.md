# 🔐 GUIDE ADMIN - Création et Gestion d'Utilisateurs

## ✅ FONCTIONNALITÉS ADMIN

L'admin peut:
- ✅ **Créer des utilisateurs** avec QR code automatique
- ✅ **Voir tous les utilisateurs** et leurs QR codes
- ✅ **Modifier les utilisateurs** (nom, email, rôle)
- ✅ **Supprimer des utilisateurs**

---

## 🚀 DÉMARRAGE

### Terminal 1 - Backend:
```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend
source /home/sahar/Bureau/Stage/venv/bin/activate
python3 app.py
```

### Terminal 2 - Frontend:
```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/frontend
npm start
```

---

## 👤 CONNEXION ADMIN

### Identifiants admin:
```
Username: admin
Password: test123
```

**Si le mot de passe ne fonctionne pas:**
```bash
cd backend
python3 -c "
import sys
sys.path.insert(0, '.')
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.password_hash = generate_password_hash('test123')
    db.session.commit()
    print('✅ Mot de passe admin réinitialisé: test123')
"
```

---

## 📝 TEST 1: CRÉER UN NOUVEL UTILISATEUR

### Étapes:

1. **Connexion:**
   - http://localhost:3000
   - Username: `admin`
   - Password: `test123`

2. **Aller à Utilisateurs:**
   - Menu → **Utilisateurs**
   - Vous verrez la liste de tous les utilisateurs avec leurs QR codes

3. **Créer un utilisateur:**
   - Cliquez **"+ Ajouter un utilisateur"**
   - Remplissez le formulaire:
     - Nom d'utilisateur: `testuser`
     - Email: `testuser@example.com`
     - Mot de passe: `test123`
     - Nom complet: `Test User`
     - Rôle: Choisissez un rôle (ex: Agent Maintenance)
   - Cliquez **"Créer"**

4. **Vérification:**

**Alert de confirmation:**
```
✅ Utilisateur créé avec succès!

👤 Nom d'utilisateur: testuser
📧 Email: testuser@example.com
🎫 QR Code: ABCD1234  ← QR code unique généré!
👥 Rôle: agent_maintenance

🔐 Mot de passe: test123

L'utilisateur peut maintenant:
• Se connecter avec son username/password
• Voir son QR code unique dans son profil
• Scanner des QR codes
```

**Liste mise à jour:**
- Le nouvel utilisateur apparaît dans le tableau
- Son QR code est affiché dans une badge coloré

**Console (F12):**
```
✅ Nouvel utilisateur créé: {
  id: 9,
  username: "testuser",
  email: "testuser@example.com",
  qr_code: "ABCD1234",
  ...
}
```

**Terminal backend:**
```
🎫 QR Code généré pour testuser: ABCD1234
✅ Utilisateur testuser créé avec QR code: ABCD1234
127.0.0.1 - - [XX:XX:XX] "POST /api/auth/register HTTP/1.1" 201 -
```

---

## 🔍 TEST 2: VÉRIFIER LE QR CODE

### Méthode 1: Dans la liste des utilisateurs

- Dans le tableau, colonne **QR Code**
- Chaque utilisateur a son code affiché
- Code en badge coloré

### Méthode 2: Base de données

```bash
cd backend
sqlite3 instance/patrimoine.db "SELECT id, username, qr_code FROM users ORDER BY id;"
```

**Résultat:**
```
1|admin|NDP9KBYG
3|samar|FARG7LJT
4|mohamed|VIJHS362
...
9|testuser|ABCD1234  ← Nouveau!
```

### Méthode 3: Vérifier l'image QR

```bash
ls -lh backend/qr_codes/qr_testuser_*
```

**Devrait montrer:**
```
-rw-r--r-- 1 user user 2.1K Nov 17 XX:XX qr_testuser_ABCD1234.png
```

---

## 👨‍💼 TEST 3: L'UTILISATEUR SE CONNECTE

### Déconnexion admin:

- Cliquez sur le bouton déconnexion

### Connexion avec le nouvel utilisateur:

```
Username: testuser
Password: test123
```

### Vérifier son profil:

- Menu → **Profile**
- Vérifications:
  - ✅ Nom affiché: "Test User"
  - ✅ Email affiché: "testuser@example.com"
  - ✅ **QR Code affiché:** ABCD1234
  - ✅ QR code scannable visible

---

## ✏️ TEST 4: MODIFIER UN UTILISATEUR (ADMIN)

### Reconnexion admin:

```
Username: admin
Password: test123
```

### Modification:

1. **Utilisateurs** → Trouver "testuser"
2. Cliquez l'icône **✏️ Modifier**
3. Changez:
   - Email: `testuser.updated@example.com`
   - Nom complet: `Test User Updated`
   - Rôle: `responsable_patrimoine`
4. Cliquez **"Mettre à jour"**

**Alert:**
```
✅ Utilisateur mis à jour avec succès!
```

**Vérification:**
- Le tableau est mis à jour
- Les nouvelles données s'affichent

---

## 🗑️ TEST 5: SUPPRIMER UN UTILISATEUR (ADMIN)

1. **Utilisateurs** → Trouver l'utilisateur à supprimer
2. Cliquez l'icône **🗑️ Supprimer**
3. Confirmez dans la popup

**Résultat:**
- L'utilisateur disparaît du tableau
- Ses données sont supprimées de la DB

---

## 📊 TABLEAU DES UTILISATEURS

### Colonnes affichées:

| Colonne | Description |
|---------|-------------|
| **Nom d'utilisateur** | Username (en gras) |
| **Email** | Adresse email |
| **Nom complet** | Nom complet de l'utilisateur |
| **Rôle** | Badge coloré avec le rôle |
| **QR Code** | Badge violet avec le code QR |
| **Date création** | Format: JJ/MM/AAAA |
| **Actions** | Boutons Modifier/Supprimer |

### Exemple:

```
┌─────────────┬──────────────────────┬───────────────┬──────────────┬──────────┬────────────┬─────────┐
│ Username    │ Email                │ Nom complet   │ Rôle         │ QR Code  │ Date       │ Actions │
├─────────────┼──────────────────────┼───────────────┼──────────────┼──────────┼────────────┼─────────┤
│ admin       │ admin@patrimoine.tn  │ Admin Sys     │ admin        │ NDP9KBYG │ 14/11/2025 │ ✏️ 🗑️   │
│ testuser    │ testuser@example.com │ Test User     │ agent_maint  │ ABCD1234 │ 17/11/2025 │ ✏️ 🗑️   │
└─────────────┴──────────────────────┴───────────────┴──────────────┴──────────┴────────────┴─────────┘
```

---

## 🎯 RÔLES DISPONIBLES

### Liste des rôles:

1. **Utilisateur** (`user`) - Utilisateur standard
2. **Administrateur** (`admin`) - Accès complet
3. **Responsable Patrimoine** (`responsable_patrimoine`)
4. **Responsable Service** (`responsable_service`)
5. **Agent Maintenance** (`agent_maintenance`)
6. **Auditeur** (`auditeur`)

Chaque rôle a des permissions différentes dans le système.

---

## ✅ CHECKLIST DE TEST ADMIN

### Création d'utilisateur:
- [ ] Admin connecté
- [ ] Page Utilisateurs affichée
- [ ] Clic "+ Ajouter un utilisateur"
- [ ] Formulaire rempli
- [ ] Utilisateur créé avec succès
- [ ] QR code généré automatiquement
- [ ] QR code affiché dans le tableau
- [ ] Alert affiche le QR code
- [ ] Console montre les détails

### Vérification utilisateur:
- [ ] Déconnexion admin
- [ ] Connexion avec nouvel utilisateur
- [ ] Profile affiché correctement
- [ ] QR code visible dans le profil
- [ ] QR code correct

### Modification:
- [ ] Reconnexion admin
- [ ] Modification réussie
- [ ] Données mises à jour dans le tableau
- [ ] Utilisateur peut se reconnecter

### Suppression:
- [ ] Suppression confirmée
- [ ] Utilisateur disparu du tableau
- [ ] Impossible de se connecter avec cet utilisateur

---

## 🐛 DÉPANNAGE

### "Nom d'utilisateur déjà utilisé"

**Cause:** Username déjà existant  
**Solution:** Choisir un autre username

### "Email déjà utilisé"

**Cause:** Email déjà existant  
**Solution:** Choisir un autre email

### "QR code non affiché dans le tableau"

**Cause:** Backend ne retourne pas le QR code  
**Solution:** 
1. Vérifier terminal backend
2. Vérifier console navigateur (F12)
3. Rafraîchir la page

### "Erreur 401 lors de la création"

**Cause:** Token JWT expiré  
**Solution:** Déconnexion/Reconnexion admin

---

## 📝 SCRIPT DE TEST RAPIDE

### Créer 5 utilisateurs de test:

```bash
cd backend
python3 -c "
import sys
sys.path.insert(0, '.')
from app import app, db, User
import requests

users_to_create = [
    {'username': 'user1', 'email': 'user1@test.com', 'full_name': 'User One', 'role': 'agent_maintenance', 'password': 'test123'},
    {'username': 'user2', 'email': 'user2@test.com', 'full_name': 'User Two', 'role': 'responsable_patrimoine', 'password': 'test123'},
    {'username': 'user3', 'email': 'user3@test.com', 'full_name': 'User Three', 'role': 'auditeur', 'password': 'test123'},
]

for user_data in users_to_create:
    response = requests.post('http://localhost:5000/api/auth/register', json=user_data)
    if response.status_code == 201:
        print(f\"✅ {user_data['username']} créé - QR: {response.json()['user']['qr_code']}\")
    else:
        print(f\"❌ Erreur pour {user_data['username']}: {response.text}\")
"
```

---

## ✅ RÉSUMÉ

**L'ADMIN PEUT:**
- ✅ Créer des utilisateurs avec QR code automatique
- ✅ Voir tous les QR codes dans le tableau
- ✅ Modifier les utilisateurs
- ✅ Supprimer les utilisateurs
- ✅ Chaque utilisateur a un QR code unique
- ✅ Les utilisateurs peuvent se connecter immédiatement
- ✅ Les QR codes sont visibles dans leur profil

**SYSTÈME COMPLET FONCTIONNEL!** 🎉
