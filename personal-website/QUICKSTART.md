# ⚡ Démarrage Rapide (5 minutes)

## Option 1: Démarrage Local (Recommandé pour le développement)

### Prérequis
- Python 3.8+
- Node.js 14+

### Étape 1: Backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python init_db.py

# Démarrer le serveur
python app.py
```

✅ Backend prêt sur `http://localhost:5000`

### Étape 2: Frontend (nouveau terminal)

```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer l'application
npm start
```

✅ Frontend prêt sur `http://localhost:3000`

### Étape 3: Connexion

```
URL: http://localhost:3000
Utilisateur: admin
Mot de passe: admin123
```

---

## Option 2: Démarrage avec Docker

### Prérequis
- Docker
- Docker Compose

### Commandes

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

✅ Application accessible sur `http://localhost`

---

## Option 3: Déploiement sur Netlify (Frontend uniquement)

### Prérequis
- Compte Netlify
- Git

### Étapes

1. **Build le frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Déployer sur Netlify**
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod --dir=build
   ```

---

## 🧪 Tests Rapides

### Vérifier le backend

```bash
curl http://localhost:5000/api/statistics
```

Vous devriez recevoir:
```json
{
  "total_assets": 12,
  "active_assets": 11,
  "total_value": 2500000,
  "by_category": [...]
}
```

### Vérifier le frontend

Ouvrez `http://localhost:3000` dans le navigateur

---

## 📊 Données de Démonstration

L'application est pré-chargée avec:
- ✅ 5 utilisateurs
- ✅ 12 actifs
- ✅ 5 maintenances
- ✅ 2 mouvements
- ✅ 3 alertes

---

## 🔐 Comptes de Test

| Rôle | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Responsable | responsable | pass123 |
| Agent | agent | pass123 |
| Auditeur | auditeur | pass123 |
| Chef Service | service_chief | pass123 |

---

## 🐛 Dépannage Rapide

### Port déjà utilisé?
```bash
# Changer le port dans app.py (ligne 100)
app.run(debug=True, port=5001)
```

### Module non trouvé?
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Base de données corrompue?
```bash
# Supprimer et recréer
rm backend/patrimoine.db
python backend/init_db.py
```

---

## 📚 Documentation Complète

- **Installation détaillée**: `INSTALLATION.md`
- **Guide d'utilisation**: `GUIDE_UTILISATION.md`
- **Scénarios détaillés**: `SCENARIOS.md`
- **Déploiement production**: `DEPLOYMENT.md`

---

## 🚀 Prochaines Étapes

1. ✅ Explorez le Tableau de Bord
2. ✅ Ajoutez un nouvel actif
3. ✅ Planifiez une maintenance
4. ✅ Générez un rapport
5. ✅ Consultez la documentation complète

---

**Bienvenue dans le système de gestion du patrimoine municipal! 🎉**
