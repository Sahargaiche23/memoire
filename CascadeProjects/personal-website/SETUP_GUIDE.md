# 🚀 Guide de Configuration Complet

## ⚠️ Erreur 401 lors de la Connexion?

Si vous recevez une erreur **401 (Unauthorized)** lors de la tentative de connexion, c'est parce que la base de données n'a pas été initialisée.

### Solution Rapide

```bash
cd backend
python init_db.py
```

Vous devriez voir:

```
✓ Tables supprimées
✓ Tables créées
✓ 5 utilisateurs créés
✓ 12 actifs créés
✓ 5 maintenances créées
✓ 2 mouvements créés
✓ 3 alertes créées

==================================================
✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS
==================================================

📊 Statistiques:
   • Utilisateurs: 5
   • Actifs: 12
   • Maintenances: 5
   • Mouvements: 2
   • Alertes: 3

🔐 Comptes de démonstration:
   • admin: admin123 (admin)
   • responsable: pass123 (responsable_patrimoine)
   • agent: pass123 (agent_maintenance)
   • auditeur: pass123 (auditeur)
   • service_chief: pass123 (responsable_service)

💡 Prochaines étapes:
   1. Démarrez le backend: python app.py
   2. Démarrez le frontend: npm start
   3. Ouvrez http://localhost:3000
   4. Connectez-vous avec les identifiants ci-dessus

==================================================
```

---

## 📋 Étapes de Configuration Complètes

### Étape 1: Backend - Installation

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Étape 2: Backend - Dépendances

```bash
# Installer les dépendances
pip install -r requirements.txt

# Vérifier que tout est installé
pip list
```

### Étape 3: Backend - Initialiser la Base de Données

```bash
# IMPORTANT: Exécuter AVANT de démarrer le serveur
python init_db.py
```

✅ Vous devriez voir le message "✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS"

### Étape 4: Backend - Démarrer le Serveur

```bash
python app.py
```

Vous devriez voir:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

✅ Backend prêt!

### Étape 5: Frontend - Installation (Nouveau Terminal)

```bash
cd frontend

# Installer les dépendances
npm install
```

### Étape 6: Frontend - Démarrer l'Application

```bash
npm start
```

Vous devriez voir:

```
Compiled successfully!

You can now view patrimoine-municipal in the browser.

  Local:            http://localhost:3000
```

✅ Frontend prêt!

### Étape 7: Accès à l'Application

Ouvrez votre navigateur et allez à:

```
http://localhost:3000
```

### Étape 8: Connexion

Utilisez l'un des comptes de démonstration:

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| admin | admin123 | Admin |
| responsable | pass123 | Responsable Patrimoine |
| agent | pass123 | Agent Maintenance |
| auditeur | pass123 | Auditeur |
| service_chief | pass123 | Responsable Service |

✅ Connecté!

---

## 🔍 Vérification de la Configuration

### Vérifier que le Backend Fonctionne

```bash
# Dans un autre terminal
curl http://localhost:5000/api/statistics
```

Vous devriez recevoir:

```json
{
  "total_assets": 12,
  "active_assets": 11,
  "total_value": 2500000,
  "by_category": {...}
}
```

### Vérifier que le Frontend Fonctionne

Ouvrez http://localhost:3000 dans votre navigateur.

Vous devriez voir la page de connexion.

### Vérifier que la Base de Données Existe

```bash
# Dans le dossier backend
ls -la patrimoine.db
```

Vous devriez voir le fichier `patrimoine.db`.

---

## 🆘 Dépannage

### Erreur: "Module not found"

```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Erreur: "Port 5000 already in use"

```bash
# Trouver le processus qui utilise le port
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
# Modifier dans app.py ligne 100:
app.run(debug=True, port=5001)
```

### Erreur: "Port 3000 already in use"

```bash
# Utiliser un autre port
PORT=3001 npm start
```

### Erreur: "Database is locked"

```bash
# Supprimer la base de données et la recréer
cd backend
rm patrimoine.db
python init_db.py
```

### Erreur 401 lors de la Connexion

```bash
# Réinitialiser la base de données
cd backend
rm patrimoine.db
python init_db.py
```

### Erreur: "CORS error"

Vérifiez que:
1. Le backend démarre sur http://127.0.0.1:5000
2. Le frontend démarre sur http://localhost:3000
3. Les deux sont en cours d'exécution

---

## 📊 Logs Importants

### Backend - Logs Normaux

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
127.0.0.1 - - [13/Nov/2025 12:59:50] "POST /api/auth/login HTTP/1.1" 200 -
```

### Frontend - Logs Normaux

```
Compiled successfully!
You can now view patrimoine-municipal in the browser.
  Local:            http://localhost:3000
```

---

## 🎯 Checklist de Configuration

- [ ] Python 3.8+ installé
- [ ] Node.js 14+ installé
- [ ] Environnement virtuel créé
- [ ] Dépendances Python installées
- [ ] Base de données initialisée (`python init_db.py`)
- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] Vous pouvez vous connecter
- [ ] Tableau de bord affiche les données

---

## 📞 Besoin d'Aide?

### Consultez:
- **QUICKSTART.md** - Démarrage rapide
- **INSTALLATION.md** - Installation détaillée
- **COMMANDS.md** - Commandes utiles
- **README.md** - Documentation complète

---

## 🔑 Points Clés à Retenir

1. **TOUJOURS exécuter `python init_db.py` avant de démarrer le backend**
2. **Utiliser les comptes de démonstration fournis**
3. **Le backend doit être sur le port 5000**
4. **Le frontend doit être sur le port 3000**
5. **Les deux doivent être en cours d'exécution**

---

**Dernière mise à jour**: Novembre 2024
