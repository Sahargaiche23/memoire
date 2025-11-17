# 🚀 COMMENCEZ ICI

Bienvenue dans le **Système de Gestion du Patrimoine Municipal**!

Ce fichier vous guide pour démarrer en quelques minutes.

---

## ⚡ Démarrage en 5 Minutes

### Prérequis
- Python 3.8+
- Node.js 14+

### Étape 1: Backend (Terminal 1)

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python init_db.py
python app.py
```

✅ Vous devriez voir: `Running on http://127.0.0.1:5000`

### Étape 2: Frontend (Terminal 2)

```bash
cd frontend
npm install
npm start
```

✅ Vous devriez voir: `You can now view patrimoine-municipal in the browser`

### Étape 3: Accès

Ouvrez votre navigateur et allez à:
```
http://localhost:3000
```

**Connexion:**
- Utilisateur: `admin`
- Mot de passe: `admin123`

✅ **C'est tout! L'application est prête!**

---

## 📚 Documentation

### Pour Commencer
1. **Ce fichier** (vous êtes ici!)
2. **QUICKSTART.md** - Démarrage rapide (5 min)
3. **GUIDE_UTILISATION.md** - Guide complet (30 min)

### Pour Approfondir
- **README.md** - Documentation complète
- **SCENARIOS.md** - Cas d'usage concrets
- **DEPLOYMENT.md** - Déploiement en production
- **INDEX.md** - Navigation complète

---

## 🎯 Prochaines Étapes

### Immédiat
1. ✅ Démarrer l'application (voir ci-dessus)
2. ✅ Se connecter avec admin/admin123
3. ✅ Explorer le Tableau de Bord

### Ensuite
1. Lire **GUIDE_UTILISATION.md**
2. Consulter **SCENARIOS.md** pour des exemples
3. Tester les fonctionnalités

### Pour la Production
1. Lire **DEPLOYMENT.md**
2. Configurer PostgreSQL
3. Mettre en place SSL

---

## 🆘 Problèmes?

### Port déjà utilisé?
```bash
# Changer le port dans backend/app.py (ligne 100)
app.run(debug=True, port=5001)
```

### Module non trouvé?
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Base de données corrompue?
```bash
cd backend
rm patrimoine.db
python init_db.py
```

### Plus d'aide?
→ Consultez **INSTALLATION.md** section "Dépannage"

---

## 📊 Données de Démonstration

L'application est pré-chargée avec:
- ✅ 5 utilisateurs (admin, responsable, agent, auditeur, service_chief)
- ✅ 12 actifs (bâtiments, véhicules, équipements, mobilier, terrains)
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

## 🎨 Fonctionnalités Principales

### Tableau de Bord
- Statistiques en temps réel
- Graphiques interactifs
- Alertes récentes

### Gestion des Actifs
- Créer, modifier, supprimer des actifs
- 5 catégories (Bâtiments, Véhicules, Équipements, Mobilier, Terrains)
- Suivi des valeurs

### Maintenances
- Planifier des maintenances
- Enregistrer les interventions
- Suivi des coûts

### Rapports
- Statistiques complètes
- Export PDF et CSV
- Graphiques

### Utilisateurs (Admin)
- Créer des comptes
- Gérer les rôles
- 5 rôles disponibles

---

## 📁 Structure du Projet

```
patrimoine-municipal/
├── backend/              # Application Flask
├── frontend/             # Application React
├── docker-compose.yml    # Configuration Docker
├── README.md             # Documentation principale
├── QUICKSTART.md         # Démarrage rapide
├── INSTALLATION.md       # Installation détaillée
├── GUIDE_UTILISATION.md  # Guide complet
├── SCENARIOS.md          # Cas d'usage
├── DEPLOYMENT.md         # Déploiement
└── ... (autres fichiers)
```

---

## 🚀 Options de Déploiement

### Option 1: Local (Recommandé pour tester)
```bash
# Suivre les étapes ci-dessus
```

### Option 2: Docker
```bash
docker-compose up -d
# Accès: http://localhost
```

### Option 3: Production
```bash
# Lire DEPLOYMENT.md
```

---

## 📞 Besoin d'Aide?

### Documentation
- **QUICKSTART.md** - Démarrage rapide
- **INSTALLATION.md** - Installation détaillée
- **GUIDE_UTILISATION.md** - Guide complet
- **COMMANDS.md** - Commandes utiles
- **INDEX.md** - Navigation complète

### Dépannage
- Consultez la section "Dépannage" dans INSTALLATION.md
- Vérifiez les logs du terminal
- Réinitialisez la base de données si nécessaire

---

## ✅ Checklist de Vérification

Après le démarrage, vérifiez que:
- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] Vous pouvez vous connecter
- [ ] Le Tableau de Bord affiche les données
- [ ] Vous pouvez voir les actifs
- [ ] Vous pouvez voir les maintenances
- [ ] Vous pouvez voir les rapports

---

## 🎉 Prêt?

1. ✅ Installez les prérequis (Python, Node.js)
2. ✅ Démarrez le backend
3. ✅ Démarrez le frontend
4. ✅ Ouvrez http://localhost:3000
5. ✅ Connectez-vous avec admin/admin123

**Bienvenue dans le système de gestion du patrimoine municipal! 🇹🇳**

---

## 📖 Lectures Recommandées

### Après le démarrage (15 minutes)
1. Explorez le Tableau de Bord
2. Consultez la page Actifs
3. Consultez la page Rapports

### Ensuite (30 minutes)
1. Lire GUIDE_UTILISATION.md
2. Consulter SCENARIOS.md
3. Tester les workflows

### Pour la Production (2-3 heures)
1. Lire DEPLOYMENT.md
2. Configurer le serveur
3. Mettre en place les sauvegardes

---

**Dernière mise à jour**: Novembre 2024  
**Version**: 1.0.0  
**Statut**: ✅ Production Ready
