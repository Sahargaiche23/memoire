# 🔧 Guide d'Installation Complet

## Prérequis Système

### Windows
- Python 3.8+ ([Télécharger](https://www.python.org/downloads/))
- Node.js 14+ ([Télécharger](https://nodejs.org/))
- Git (optionnel)

### macOS
```bash
# Installer Homebrew si nécessaire
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Python et Node.js
brew install python@3.11 node
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3.11 python3-pip nodejs npm
```

---

## 📦 Installation Étape par Étape

### Étape 1: Préparer l'environnement

```bash
# Créer le répertoire du projet
mkdir patrimoine-municipal
cd patrimoine-municipal

# Cloner ou télécharger le projet
# (Si vous avez un repository Git)
# git clone <url-du-repo>
```

### Étape 2: Configuration du Backend

```bash
# Naviguer vers le dossier backend
cd backend

# Créer un environnement virtuel Python
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données avec données de démonstration
python init_db.py
```

**Résultat attendu:**
```
✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS
📊 Statistiques:
   • Utilisateurs: 5
   • Actifs: 12
   • Maintenances: 5
   • Mouvements: 2
   • Alertes: 3
```

### Étape 3: Démarrer le Backend

```bash
# Depuis le dossier backend (avec venv activé)
python app.py
```

**Résultat attendu:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

✅ Le backend est maintenant en cours d'exécution sur `http://localhost:5000`

### Étape 4: Configuration du Frontend

```bash
# Ouvrir un nouveau terminal
# Naviguer vers le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm start
```

**Résultat attendu:**
```
Compiled successfully!

You can now view patrimoine-municipal in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

✅ Le frontend est maintenant accessible sur `http://localhost:3000`

---

## 🚀 Première Utilisation

### Accès à l'Application

1. Ouvrez votre navigateur
2. Allez à `http://localhost:3000`
3. Vous verrez l'écran de connexion

### Connexion

Utilisez l'un des comptes de démonstration:

```
Admin:
  Utilisateur: admin
  Mot de passe: admin123

Responsable:
  Utilisateur: responsable
  Mot de passe: pass123

Agent:
  Utilisateur: agent
  Mot de passe: pass123
```

### Vérification du Fonctionnement

1. ✅ Connectez-vous avec le compte admin
2. ✅ Vous devriez voir le Tableau de Bord
3. ✅ Cliquez sur "Actifs" - vous devriez voir 12 actifs
4. ✅ Cliquez sur "Maintenance" - vous devriez voir 5 maintenances
5. ✅ Cliquez sur "Rapports" - vous devriez voir les statistiques

---

## 🐛 Dépannage

### Problème: "Port 5000 déjà utilisé"

```bash
# Trouver le processus utilisant le port
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Terminer le processus ou utiliser un autre port
# Dans app.py, changez:
app.run(debug=True, port=5001)  # Utiliser le port 5001
```

### Problème: "Module Flask non trouvé"

```bash
# Vérifier que l'environnement virtuel est activé
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Problème: "npm: command not found"

```bash
# Vérifier que Node.js est installé
node --version
npm --version

# Si non installé, télécharger depuis https://nodejs.org/
```

### Problème: "Erreur de connexion au backend"

```bash
# Vérifier que le backend est en cours d'exécution
curl http://localhost:5000/api/statistics

# Si erreur, vérifier les logs du backend
# Vérifier que CORS est activé dans app.py
```

### Problème: "Base de données corrompue"

```bash
# Supprimer la base de données
rm patrimoine.db  # macOS/Linux
del patrimoine.db  # Windows

# Réinitialiser
python init_db.py
```

---

## 📁 Structure des Fichiers

```
patrimoine-municipal/
├── backend/
│   ├── app.py                 # Application Flask
│   ├── init_db.py             # Script d'initialisation
│   ├── requirements.txt       # Dépendances Python
│   ├── .env                   # Configuration
│   ├── venv/                  # Environnement virtuel
│   └── patrimoine.db          # Base de données SQLite
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Assets.js
│   │   │   ├── Maintenance.js
│   │   │   ├── Users.js
│   │   │   ├── Reports.js
│   │   │   └── [fichiers CSS]
│   │   └── components/
│   │       └── Navbar.js
│   ├── package.json
│   ├── node_modules/
│   └── .gitignore
│
├── README.md                  # Documentation principale
├── GUIDE_UTILISATION.md       # Guide d'utilisation
└── INSTALLATION.md            # Ce fichier
```

---

## 🔐 Configuration de Sécurité

### Avant la Production

1. **Changer la clé secrète JWT**
   ```python
   # Dans backend/.env
   JWT_SECRET_KEY=your-super-secret-key-change-in-production-2024
   # Remplacer par une clé forte et aléatoire
   ```

2. **Configurer la base de données**
   ```python
   # Pour PostgreSQL en production:
   DATABASE_URL=postgresql://user:password@localhost/patrimoine
   ```

3. **Activer HTTPS**
   ```python
   # Utiliser un certificat SSL
   # Configurer un reverse proxy (Nginx, Apache)
   ```

4. **Sauvegarder les données**
   ```bash
   # Sauvegarder régulièrement la base de données
   cp patrimoine.db patrimoine_backup_$(date +%Y%m%d).db
   ```

---

## 📊 Vérification de l'Installation

### Checklist

- [ ] Python 3.8+ installé
- [ ] Node.js 14+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances Python installées
- [ ] Base de données initialisée
- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] Connexion possible avec admin/admin123
- [ ] Tableau de bord affiche les données
- [ ] Tous les menus sont accessibles

---

## 🚀 Prochaines Étapes

1. **Lire le guide d'utilisation**: `GUIDE_UTILISATION.md`
2. **Créer des comptes utilisateurs**: Accédez à "Utilisateurs" (Admin)
3. **Ajouter des actifs**: Accédez à "Actifs"
4. **Planifier des maintenances**: Accédez à "Maintenance"
5. **Générer des rapports**: Accédez à "Rapports"

---

## 📞 Support

Si vous rencontrez des problèmes:

1. Vérifiez les logs du terminal
2. Consultez la section Dépannage
3. Vérifiez que tous les prérequis sont installés
4. Essayez de réinitialiser la base de données

---

**Installation terminée! Bienvenue dans le système de gestion du patrimoine municipal. 🎉**
