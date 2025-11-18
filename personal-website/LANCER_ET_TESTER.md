# 🚀 GUIDE RAPIDE - Lancer et Tester le Système

## ⚡ DÉMARRAGE RAPIDE (3 commandes)

### Terminal 1: Backend
```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend
source /home/sahar/Bureau/Stage/venv/bin/activate
python3 app.py
```

**Attendez de voir:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Terminal 2: Frontend
```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website/frontend
npm start
```

**Le navigateur s'ouvrira automatiquement sur:** http://localhost:3000

---

### Terminal 3: Tests automatiques
```bash
cd ~/Bureau/ERPM2/CascadeProjects/personal-website
./START_AND_TEST.sh
```

**Vous verrez:**
```
✅ Connexion réussie!
✅ Modification réussie!
✅ Upload réussi!
✅ Tests terminés!
```

---

## 🧪 TEST MANUEL (Interface Web)

### 1. **Connexion**
- Allez à: http://localhost:3000
- Username: `sahar`
- Password: `test123`

### 2. **Test Modification de Profil**

1. Cliquez sur **Profile** dans le menu
2. Cliquez sur **"✏️ Modifier le Profil"**
3. Changez:
   - Nom: `Votre Nouveau Nom`
   - Email: `nouveau@email.com`
4. Cliquez **"💾 Enregistrer"**

**✅ Résultat attendu:**
- Alert: "Profil mis à jour avec succès!"
- Page recharge
- Nouveau nom affiché
- Nouvel email affiché

**📊 Vérifier en DB:**
```bash
cd backend
sqlite3 instance/patrimoine.db "SELECT username, full_name, email FROM users WHERE username='sahar';"
```

---

### 3. **Test Upload d'Image**

1. Dans la page **Profile**
2. **Cliquez sur l'avatar** (cercle avec icône)
3. **Sélectionnez une image** (JPG, PNG, GIF)
4. Attendez l'upload

**✅ Résultat attendu:**
- Alert: "Photo de profil uploadée et sauvegardée!"
- Page recharge
- Votre image s'affiche dans l'avatar
- L'image reste après F5 (rafraîchir)

**📊 Vérifier fichier:**
```bash
cd backend
ls -lh uploads/profile_7_*
```

---

### 4. **Test Persistance**

1. **Déconnectez-vous**
2. **Fermez le navigateur**
3. **Rouvrez** http://localhost:3000
4. **Reconnectez-vous:** sahar / test123
5. **Vérifiez Profile**

**✅ Résultat attendu:**
- Nom modifié toujours affiché ✅
- Email modifié toujours affiché ✅
- Image de profil toujours affichée ✅
- QR Code affiché ✅

---

## 📋 COMMANDES UTILES

### Vérifier que les serveurs fonctionnent:
```bash
# Backend (port 5000)
curl http://localhost:5000/api/auth/login

# Frontend (port 3000)
curl http://localhost:3000
```

### Voir tous les utilisateurs:
```bash
cd backend
sqlite3 instance/patrimoine.db "SELECT id, username, full_name, email FROM users;"
```

### Voir les images uploadées:
```bash
cd backend
ls -lh uploads/profile_*
```

### Réinitialiser le mot de passe d'un utilisateur:
```bash
cd backend
python3 fix_sahar_password.py
```

---

## ⚠️ PROBLÈMES COURANTS

### "Port 5000 already in use"
```bash
# Trouver et arrêter le processus
lsof -ti:5000 | xargs kill -9
```

### "Port 3000 already in use"
```bash
# Trouver et arrêter le processus
lsof -ti:3000 | xargs kill -9
```

### "Modification ne s'enregistre pas"
1. F12 → Console → Vérifier erreurs
2. Ctrl+Shift+Delete → Effacer cache
3. Déconnexion/Reconnexion

### "Image ne s'affiche pas"
1. Vérifier: `ls backend/uploads/profile_*`
2. Ctrl+F5 (rafraîchir avec cache vidé)
3. Vérifier console (F12) pour erreurs

---

## ✅ CHECKLIST RAPIDE

Avant de commencer:
- [ ] Terminal 1: Backend démarré (port 5000)
- [ ] Terminal 2: Frontend démarré (port 3000)
- [ ] Navigateur ouvert: http://localhost:3000

Tests de base:
- [ ] Connexion fonctionne
- [ ] Page Profile s'affiche
- [ ] Modification de nom fonctionne
- [ ] Modification d'email fonctionne
- [ ] Upload d'image fonctionne
- [ ] Données persistées après reconnexion

---

## 🎯 RÉSULTAT ATTENDU

Si tout fonctionne correctement:
- ✅ Vous pouvez modifier votre nom
- ✅ Vous pouvez modifier votre email
- ✅ Vous pouvez uploader une image
- ✅ Tout est sauvegardé en base de données
- ✅ Tout reste après déconnexion/reconnexion
- ✅ Aucune erreur dans les consoles

**SYSTÈME 100% FONCTIONNEL!** 🎉

---

## 📚 FICHIERS DE RÉFÉRENCE

- **Guide complet:** `TEST_FINAL_COMPLET.md`
- **Test automatique:** `backend/test_profile_complet.py`
- **Script de démarrage:** `START_AND_TEST.sh`
- **Tests utilisateurs:** `TEST_TOUS_LES_USERS.md`

---

**COMMENCEZ PAR LANCER LES 3 TERMINAUX CI-DESSUS!** 🚀
