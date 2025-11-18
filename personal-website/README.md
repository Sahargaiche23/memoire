# 🇹🇳 Système de Gestion du Patrimoine Municipal

Un système complet et moderne de gestion du patrimoine municipal avec interface web intuitive, conçu pour les municipalités tunisiennes.

## 📋 Table des matières

- [Caractéristiques](#caractéristiques)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Scénarios d'utilisation](#scénarios-dutilisation)
- [Guide détaillé](#guide-détaillé)
- [API Documentation](#api-documentation)

## ✨ Caractéristiques

### Fonctionnalités principales

- **Gestion des Actifs** - Enregistrement, modification et suivi complet des biens municipaux
- **Gestion des Utilisateurs** - Système de rôles et permissions (Admin, Responsable, Agent, Auditeur)
- **Planification de Maintenance** - Maintenances préventives et correctives
- **Mouvements d'Actifs** - Suivi des transferts entre services et sites
- **Rapports et Statistiques** - Génération de rapports PDF/CSV avec graphiques
- **Alertes Automatiques** - Notifications pour garanties, maintenances et amortissements
- **Authentification Sécurisée** - JWT avec gestion des sessions
- **Interface Responsive** - Design moderne adapté à tous les appareils

### Catégories d'Actifs

- Bâtiments
- Véhicules
- Équipements
- Mobilier
- Terrains

### Rôles Utilisateurs

| Rôle | Permissions |
|------|-------------|
| **Admin** | Accès complet, gestion des utilisateurs |
| **Responsable Patrimoine** | Gestion complète des actifs, rapports |
| **Responsable Service** | Demande de transferts, consultation |
| **Agent Maintenance** | Enregistrement des interventions |
| **Auditeur** | Consultation des rapports et statistiques |

## 🏗️ Architecture

```
patrimoine-municipal/
├── backend/
│   ├── app.py                 # Application Flask principale
│   ├── requirements.txt       # Dépendances Python
│   └── .env                   # Configuration
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── App.js
    │   ├── App.css
    │   ├── index.js
    │   ├── pages/
    │   │   ├── Login.js
    │   │   ├── Dashboard.js
    │   │   ├── Assets.js
    │   │   ├── Maintenance.js
    │   │   ├── Users.js
    │   │   ├── Reports.js
    │   │   └── [styles CSS]
    │   └── components/
    │       └── Navbar.js
    └── package.json
```

### Stack Technologique

**Backend:**
- Python 3.8+
- Flask 2.3.3
- SQLAlchemy 2.0
- JWT Authentication
- SQLite/PostgreSQL

**Frontend:**
- React 18.2
- React Router 6
- Axios
- Recharts (Graphiques)
- Lucide React (Icônes)

## 🚀 Installation

### Prérequis

- Python 3.8+
- Node.js 14+
- npm ou yarn

### Backend Setup

```bash
# 1. Naviguer vers le dossier backend
cd backend

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser la base de données
python app.py

# 5. Le serveur démarre sur http://localhost:5000
```

### Frontend Setup

```bash
# 1. Naviguer vers le dossier frontend
cd frontend

# 2. Installer les dépendances
npm install

# 3. Démarrer le serveur de développement
npm start

# 4. L'application s'ouvre sur http://localhost:3000
```

## 📖 Utilisation

### Accès à l'Application

1. Ouvrez http://localhost:3000
2. Connectez-vous avec les identifiants de démonstration:

| Rôle | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Responsable | responsable | pass123 |
| Agent | agent | pass123 |

### Navigation Principale

- **Tableau de Bord** - Vue d'ensemble des statistiques et alertes
- **Actifs** - Gestion complète des biens municipaux
- **Maintenance** - Planification et suivi des maintenances
- **Utilisateurs** - Gestion des comptes (Admin uniquement)
- **Rapports** - Génération de rapports et statistiques

## 🎯 Scénarios d'Utilisation

### Scénario 1: Enregistrement d'un nouvel actif

**Acteur:** Responsable du Patrimoine

**Étapes:**
1. Accédez à la page "Actifs"
2. Cliquez sur "Ajouter un actif"
3. Remplissez les informations:
   - Nom: "Bâtiment Mairie"
   - Catégorie: "Bâtiment"
   - Localisation: "Centre-ville"
   - Valeur d'acquisition: "500000 DT"
   - Date d'acquisition: "2020-01-15"
4. Cliquez sur "Créer"

**Résultat:** L'actif est enregistré et visible dans la liste

---

### Scénario 2: Planifier une maintenance préventive

**Acteur:** Responsable du Patrimoine

**Étapes:**
1. Accédez à "Maintenance"
2. Cliquez sur "Planifier une maintenance"
3. Sélectionnez l'actif: "Bâtiment Mairie"
4. Type: "Préventive"
5. Date prévue: "2024-12-01"
6. Coût estimé: "5000 DT"
7. Description: "Inspection annuelle et nettoyage"
8. Cliquez sur "Créer"

**Résultat:** La maintenance est planifiée et apparaît dans le calendrier

---

### Scénario 3: Enregistrer une intervention de maintenance

**Acteur:** Agent de Maintenance

**Étapes:**
1. Accédez à "Maintenance"
2. Cliquez sur l'icône d'édition de la maintenance planifiée
3. Changez le statut à "En cours"
4. Mettez à jour le coût réel: "4800 DT"
5. Cliquez sur "Mettre à jour"
6. Une fois terminée, changez le statut à "Complétée"
7. Entrez la date de complétion

**Résultat:** L'intervention est enregistrée dans l'historique

---

### Scénario 4: Générer un rapport d'inventaire

**Acteur:** Responsable du Patrimoine / Auditeur

**Étapes:**
1. Accédez à "Rapports"
2. Consultez les statistiques affichées:
   - Total des actifs
   - Valeur totale du patrimoine
   - Distribution par catégorie
3. Cliquez sur "Exporter en PDF" ou "Exporter en CSV"
4. Le fichier est téléchargé

**Résultat:** Un rapport complet est généré avec tous les détails

---

### Scénario 5: Transférer un actif entre services

**Acteur:** Responsable de Service

**Étapes:**
1. Accédez à "Actifs"
2. Sélectionnez l'actif à transférer
3. Modifiez la localisation: "Service des Travaux Publics"
4. Mettez à jour le responsable assigné
5. Cliquez sur "Mettre à jour"

**Résultat:** Le mouvement est enregistré et tracé

---

### Scénario 6: Gérer les utilisateurs (Admin)

**Acteur:** Administrateur

**Étapes:**
1. Accédez à "Utilisateurs"
2. Cliquez sur "Ajouter un utilisateur"
3. Remplissez:
   - Nom d'utilisateur: "ali_ben"
   - Email: "ali@municipality.tn"
   - Mot de passe: "SecurePass123"
   - Nom complet: "Ali Ben Ahmed"
   - Rôle: "Agent Maintenance"
4. Cliquez sur "Créer"

**Résultat:** Le nouvel utilisateur peut se connecter

---

## 📚 Guide Détaillé

### Gestion des Actifs

#### Ajouter un Actif

```
Formulaire d'ajout:
- Nom* (obligatoire): Identifiant unique de l'actif
- Catégorie*: Bâtiment, Véhicule, Équipement, Mobilier, Terrain
- Description: Détails supplémentaires
- Date d'acquisition: Format YYYY-MM-DD
- Valeur d'acquisition: Montant initial en DT
- Valeur actuelle: Valeur actuelle (après amortissement)
- Localisation: Adresse ou site
- Statut: Actif, Maintenance, Hors service, Déclassé
- Assigné à: Responsable de l'actif
```

#### Modifier un Actif

1. Cliquez sur l'icône d'édition (✏️)
2. Modifiez les champs souhaités
3. Cliquez sur "Mettre à jour"

#### Supprimer un Actif

1. Cliquez sur l'icône de suppression (🗑️)
2. Confirmez la suppression

### Gestion des Maintenances

#### Planifier une Maintenance

```
Informations requises:
- Actif*: Sélectionner dans la liste
- Type*: Préventive ou Corrective
- Date prévue*: Date planifiée
- Description: Détails de l'intervention
- Coût estimé: Budget prévu
- Statut: Planifiée, En cours, Complétée
```

#### Statuts de Maintenance

- **Planifiée**: En attente d'exécution
- **En cours**: Intervention en cours
- **Complétée**: Intervention terminée

### Rapports et Statistiques

#### Tableaux de Bord

Le tableau de bord affiche:
- Nombre total d'actifs
- Nombre d'actifs actifs
- Valeur totale du patrimoine
- Nombre d'alertes
- Graphiques de distribution par catégorie

#### Exports

**Format PDF:**
- Rapport complet avec statistiques
- Liste détaillée des actifs
- Historique des maintenances

**Format CSV:**
- Données structurées pour Excel
- Facilite l'analyse externe
- Compatible avec tous les outils

### Alertes et Notifications

Les alertes sont générées automatiquement pour:
- **Maintenance**: Rappel avant la date prévue
- **Garantie**: Notification avant expiration
- **Amortissement**: Alerte sur la valeur résiduelle

## 🔌 API Documentation

### Authentification

**POST** `/api/auth/login`
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Réponse:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@municipality.tn",
    "role": "admin",
    "full_name": "Administrateur"
  }
}
```

### Actifs

**GET** `/api/assets` - Récupérer tous les actifs

**POST** `/api/assets` - Créer un nouvel actif
```json
{
  "name": "Bâtiment Mairie",
  "category": "bâtiment",
  "location": "Centre-ville",
  "acquisition_value": 500000,
  "current_value": 450000,
  "status": "actif"
}
```

**PUT** `/api/assets/<id>` - Modifier un actif

**DELETE** `/api/assets/<id>` - Supprimer un actif

### Maintenances

**GET** `/api/maintenances` - Récupérer toutes les maintenances

**POST** `/api/maintenances` - Planifier une maintenance
```json
{
  "asset_id": 1,
  "maintenance_type": "préventive",
  "scheduled_date": "2024-12-01",
  "cost": 5000,
  "status": "planifiée"
}
```

**PUT** `/api/maintenances/<id>` - Mettre à jour une maintenance

### Statistiques

**GET** `/api/statistics` - Récupérer les statistiques globales

**Réponse:**
```json
{
  "total_assets": 45,
  "active_assets": 42,
  "total_value": 2500000,
  "by_category": [
    {"category": "bâtiment", "count": 15},
    {"category": "véhicule", "count": 8}
  ]
}
```

## 🔐 Sécurité

- **JWT Authentication**: Tokens sécurisés avec expiration
- **Password Hashing**: Utilisation de Werkzeug pour le hachage
- **CORS Enabled**: Configuration sécurisée des origines
- **Role-Based Access**: Contrôle d'accès par rôle

## 📱 Responsive Design

L'application est optimisée pour:
- Desktop (1920px+)
- Tablette (768px - 1024px)
- Mobile (320px - 767px)

## 🐛 Dépannage

### Le backend ne démarre pas

```bash
# Vérifiez que Python est installé
python --version

# Vérifiez les dépendances
pip list | grep Flask

# Réinstallez les dépendances
pip install -r requirements.txt --force-reinstall
```

### Le frontend ne se connecte pas au backend

```bash
# Vérifiez que le backend est en cours d'exécution
curl http://localhost:5000/api/statistics

# Vérifiez la configuration CORS dans app.py
# Assurez-vous que http://localhost:3000 est autorisé
```

### Erreur de base de données

```bash
# Supprimez la base de données existante
rm patrimoine.db

# Redémarrez l'application pour recréer la BD
python app.py
```

## 📞 Support

Pour toute question ou problème, veuillez:
1. Vérifier la documentation
2. Consulter les logs d'erreur
3. Vérifier la configuration

## 📄 Licence

Ce projet est fourni à titre d'exemple pour les municipalités tunisiennes.

---

**Développé avec ❤️ pour la gestion efficace du patrimoine municipal**
