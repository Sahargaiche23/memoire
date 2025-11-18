# 📸 GUIDE COMPLET - CAPTURES D'ÉCRAN

## 🚀 PRÉPARATION

### Étape 1: Lancez l'Application

**Terminal 1 - Backend:**
```bash
cd /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/frontend
npm start
```

**Vérifiez:**
- ✅ Backend sur http://localhost:5000
- ✅ Frontend sur http://localhost:3000

### Étape 2: Préparez l'Outil de Capture

**Linux (Ubuntu):**
- Appuyez sur `PrtScn` pour tout l'écran
- Ou utilisez **Flameshot**: `sudo apt install flameshot`
- Raccourci: `Shift + PrtScn`

**Windows:**
- Utilisez **Snipping Tool** (Outil Capture d'écran)
- Ou `Win + Shift + S`

**MacOS:**
- `Cmd + Shift + 4` pour sélection
- `Cmd + Shift + 3` pour tout l'écran

---

## 📋 LISTE DES 25 CAPTURES À PRENDRE

### 🔐 SPRINT 1: ADMINISTRATEUR (5 captures)

#### Capture 1: Page de Connexion
**Nom:** `figure_3_7_page_login.png`

**URL:** http://localhost:3000/login

**Ce qui doit apparaître:**
- Logo/Titre "Patrimoine Municipal"
- Formulaire avec:
  - Champ Email
  - Champ Mot de passe
  - Bouton "Se connecter"
- Design propre et centré

**Astuces:**
- Laissez les champs vides ou remplis avec des données tests
- Cadrez bien le formulaire au centre
- Pas de barre d'outils du navigateur si possible (F11)

---

#### Capture 2: Dashboard Administrateur
**Nom:** `figure_3_8_dashboard_admin.png`

**URL:** http://localhost:3000/dashboard

**Connexion:** admin@ville.tn / admin123

**Ce qui doit apparaître:**
- En-tête avec "Bienvenue, Admin Système"
- 4 cartes statistiques:
  - Actifs Total (7)
  - Actifs Actifs (7)
  - Valeur Totale (222M DT)
  - Alertes (nombre)
- 2 graphiques:
  - Pie Chart (Distribution par catégorie)
  - Bar Chart (Actifs par catégorie)
- Section alertes récentes (5 alertes)

**Astuces:**
- Scroll vers le haut pour voir tout le dashboard
- Assurez-vous que les graphiques sont bien visibles
- Les alertes doivent être affichées (lancez `python3 create_test_alerts.py` si besoin)

---

#### Capture 3: Liste des Utilisateurs
**Nom:** `figure_3_9_liste_utilisateurs.png`

**URL:** http://localhost:3000/users

**Ce qui doit apparaître:**
- Tableau avec colonnes:
  - Nom complet
  - Email
  - Rôle
  - Date création
  - Actions (Modifier, Supprimer)
- Bouton "Ajouter Utilisateur"
- Au moins 2-3 utilisateurs dans la liste

**Astuces:**
- Si la page n'existe pas encore, prenez la capture du Dashboard
- Ou créez une capture Postman de GET /api/users

---

#### Capture 4: Formulaire Ajouter Utilisateur
**Nom:** `figure_3_10_ajouter_utilisateur.png`

**Ce qui doit apparaître:**
- Modal ou page avec formulaire:
  - Nom complet
  - Email
  - Rôle (dropdown: admin, manager, technician)
  - Mot de passe
  - Bouton "Enregistrer"

---

#### Capture 5: Liste des Catégories
**Nom:** `figure_3_11_liste_categories.png`

**URL:** http://localhost:3000/categories

**Ce qui doit apparaître:**
- Liste des catégories:
  - Mobilier
  - Véhicule
  - Terrain
  - Équipement
- Bouton "Ajouter Catégorie"

---

### 📦 SPRINT 2: GESTIONNAIRE (6 captures)

#### Capture 6: Liste des Actifs
**Nom:** `figure_4_5_liste_actifs.png`

**URL:** http://localhost:3000/assets

**Ce qui doit apparaître:**
- Tableau des actifs avec:
  - Nom
  - Catégorie
  - Valeur
  - Statut
  - Localisation
  - Actions
- Filtres (par catégorie, statut)
- Barre de recherche
- Bouton "Ajouter Actif"
- Au moins 5-7 actifs visibles

**Astuces:**
- Montrez des actifs de différentes catégories
- Différents statuts (actif, maintenance, etc.)

---

#### Capture 7: Détails d'un Actif
**Nom:** `figure_4_6_details_actif.png`

**URL:** http://localhost:3000/assets/1

**Ce qui doit apparaître:**
- Informations complètes de l'actif:
  - Nom
  - Catégorie
  - Description
  - Valeur
  - Date d'achat
  - Localisation
  - Statut
- Historique des maintenances
- Boutons "Modifier", "Supprimer", "Planifier Maintenance"

---

#### Capture 8: Formulaire Ajouter Actif
**Nom:** `figure_4_7_ajouter_actif.png`

**URL:** http://localhost:3000/assets/new

**Ce qui doit apparaître:**
- Formulaire avec tous les champs:
  - Nom
  - Catégorie (dropdown)
  - Description
  - Valeur (DT)
  - Date d'achat
  - Localisation
  - Statut
- Bouton "Enregistrer"

---

#### Capture 9: Formulaire Modifier Actif
**Nom:** `figure_4_8_modifier_actif.png`

**URL:** http://localhost:3000/assets/1/edit

**Ce qui doit apparaître:**
- Formulaire pré-rempli avec les données de l'actif
- Même structure que l'ajout
- Bouton "Mettre à jour"

---

#### Capture 10: Planifier une Maintenance
**Nom:** `figure_4_9_planifier_maintenance.png`

**URL:** http://localhost:3000/maintenances/new

**Ce qui doit apparaître:**
- Formulaire:
  - Sélection actif (dropdown)
  - Type (préventive/corrective)
  - Date planifiée
  - Description
  - Coût estimé
- Bouton "Planifier"

---

#### Capture 11: Liste des Maintenances
**Nom:** `figure_4_10_liste_maintenances.png`

**URL:** http://localhost:3000/maintenances

**Ce qui doit apparaître:**
- Tableau des maintenances:
  - Actif
  - Type
  - Date planifiée
  - Statut (planifié, en_cours, terminé)
  - Coût
  - Actions
- Filtres par statut
- Au moins 5 maintenances

---

### 🔧 SPRINT 3: MAINTENANCES & ALERTES (4 captures)

#### Capture 12: Alertes sur Dashboard
**Nom:** `figure_5_5_alertes_dashboard.png`

**URL:** http://localhost:3000/dashboard

**Focus:** Section "Alertes Récentes"

**Ce qui doit apparaître:**
- 5 alertes affichées avec:
  - Icône ⚠️ ou 🔔
  - Type d'alerte (MAINTENANCE)
  - Message clair:
    - "⚠️ Maintenance en retard: Bus 01 (2 jours)"
    - "Maintenance prévue: Camion dans 2 jours"
  - Date
  - Statut (Non lue / Lue)
- Bouton refresh 🔄

**Astuces:**
- **IMPORTANT:** Lancez d'abord le script pour créer des alertes:
```bash
cd backend
python3 create_test_alerts.py
```
- Cliquez sur 🔄 pour actualiser
- Vous devriez voir 5 alertes

---

#### Capture 13: Statistiques et Graphiques
**Nom:** `figure_5_6_statistiques_graphiques.png`

**URL:** http://localhost:3000/dashboard

**Focus:** Section graphiques

**Ce qui doit apparaître:**
- Pie Chart coloré (Distribution par catégorie)
- Bar Chart (Actifs par catégorie)
- Légendes claires
- Couleurs distinctes

---

#### Capture 14: Mouvements d'Actifs
**Nom:** `figure_5_7_mouvements_actifs.png`

**Ce qui doit apparaître:**
- Historique des mouvements:
  - Date
  - Actif
  - Type de mouvement
  - De → Vers
  - Utilisateur

*Si cette page n'existe pas, prenez une capture alternative du Dashboard*

---

#### Capture 15: Historique Maintenances
**Nom:** `figure_5_8_historique_maintenances.png`

**URL:** http://localhost:3000/maintenances?status=terminé

**Ce qui doit apparaître:**
- Liste des maintenances terminées
- Filtres appliqués
- Dates de réalisation
- Coûts finaux

---

### 💬 SPRINT 4: MESSAGERIE (5 captures)

#### Capture 16: Messenger Principal
**Nom:** `figure_6_5_messenger_principal.png`

**URL:** http://localhost:3000/messenger

**Ce qui doit apparaître:**
- Interface avec 3 colonnes:
  1. **Gauche:** Liste conversations
     - Utilisateurs
     - Groupes
     - Dernier message
  2. **Centre:** Zone de chat
     - Messages
     - Input en bas
  3. **Droite:** Détails conversation

---

#### Capture 17: Conversation 1-1
**Nom:** `figure_6_6_conversation_1_1.png`

**URL:** http://localhost:3000/messenger

**Focus:** Conversation active avec un utilisateur

**Ce qui doit apparaître:**
- Nom de l'utilisateur en haut
- Messages avec:
  - Bulles différentes (envoyé/reçu)
  - Timestamps
  - Avatar (si disponible)
- Input message en bas
- Bouton envoyer
- Au moins 5-10 messages dans la conversation

---

#### Capture 18: Groupe de Discussion
**Nom:** `figure_6_7_groupe_discussion.png`

**URL:** http://localhost:3000/messenger

**Focus:** Groupe actif

**Ce qui doit apparaître:**
- Nom du groupe en haut
- Messages avec nom de l'expéditeur
- Membres du groupe affichés (droite)
- Messages de plusieurs utilisateurs

---

#### Capture 19: Créer un Groupe
**Nom:** `figure_6_8_creer_groupe.png`

**URL:** http://localhost:3000/messenger

**Ce qui doit apparaître:**
- Modal "Créer un Groupe"
- Champ "Nom du groupe"
- Liste de checkboxes pour sélectionner membres
- Bouton "Créer"

---

#### Capture 20: Notifications
**Nom:** `figure_6_9_notifications.png`

**Ce qui doit apparaître:**
- Panel ou dropdown de notifications
- Liste des notifications non lues
- Badge avec nombre

---

### 🧪 TESTS POSTMAN (5 captures)

#### Test 1: Login
**Nom:** `figure_test_1_login.png`

**Postman Request:**
```
POST http://localhost:5000/api/login
Body: {
  "email": "admin@ville.tn",
  "password": "admin123"
}
```

**Ce qui doit apparaître:**
- Request complète
- Response 200 OK
- Token JWT dans la réponse
- User object

---

#### Test 2: Créer Actif
**Nom:** `figure_test_2_create_asset.png`

**Postman Request:**
```
POST http://localhost:5000/api/assets
Headers: Authorization: Bearer {token}
Body: {
  "name": "Nouveau Bus",
  "category_id": 1,
  "value": 180000,
  "status": "actif"
}
```

**Response:** 201 Created

---

#### Test 3: GET Alertes
**Nom:** `figure_test_3_get_alerts.png`

**Postman Request:**
```
GET http://localhost:5000/api/alerts
Headers: Authorization: Bearer {token}
```

**Ce qui doit apparaître:**
- Array d'alertes
- Au moins 5 alertes
- Structure complète de chaque alerte

---

#### Test 4: Envoyer Message
**Nom:** `figure_test_4_send_message.png`

**Postman Request:**
```
POST http://localhost:5000/api/messages
Headers: Authorization: Bearer {token}
Body: {
  "receiver_id": 2,
  "content": "Bonjour, le bus est prêt!"
}
```

**Response:** 201 Created

---

#### Test 5: Créer Groupe
**Nom:** `figure_test_5_create_group.png`

**Postman Request:**
```
POST http://localhost:5000/api/groups
Headers: Authorization: Bearer {token}
Body: {
  "name": "Équipe Maintenance",
  "members": [2, 3, 4]
}
```

**Response:** 201 Created

---

## 📐 CONSEILS POUR DE BELLES CAPTURES

### 1. Résolution
- **Minimum:** 1920x1080 (Full HD)
- Évitez les captures floues

### 2. Cadrage
- Centrez le contenu principal
- Évitez les barres de navigation du navigateur (F11)
- Pas de distractions (fermer onglets inutiles)

### 3. Données
- Utilisez des données réalistes
- Pas de "test test test"
- Noms cohérents en français

### 4. Interface
- Zoom à 100% (Ctrl+0)
- Mode clair de préférence
- Pas de mode développeur (F12) ouvert

### 5. Format
- Enregistrez en **PNG** (meilleure qualité)
- Pas de JPEG (compression)

---

## ✅ CHECKLIST COMPLÈTE

### Préparation:
- [ ] Backend lancé (port 5000)
- [ ] Frontend lancé (port 3000)
- [ ] Test alerts créés (`python3 create_test_alerts.py`)
- [ ] Connecté en tant qu'admin
- [ ] Outil de capture prêt

### Sprint 1 (5 captures):
- [ ] figure_3_7_page_login.png
- [ ] figure_3_8_dashboard_admin.png
- [ ] figure_3_9_liste_utilisateurs.png
- [ ] figure_3_10_ajouter_utilisateur.png
- [ ] figure_3_11_liste_categories.png

### Sprint 2 (6 captures):
- [ ] figure_4_5_liste_actifs.png
- [ ] figure_4_6_details_actif.png
- [ ] figure_4_7_ajouter_actif.png
- [ ] figure_4_8_modifier_actif.png
- [ ] figure_4_9_planifier_maintenance.png
- [ ] figure_4_10_liste_maintenances.png

### Sprint 3 (4 captures):
- [ ] figure_5_5_alertes_dashboard.png ⭐
- [ ] figure_5_6_statistiques_graphiques.png
- [ ] figure_5_7_mouvements_actifs.png
- [ ] figure_5_8_historique_maintenances.png

### Sprint 4 (5 captures):
- [ ] figure_6_5_messenger_principal.png ⭐
- [ ] figure_6_6_conversation_1_1.png
- [ ] figure_6_7_groupe_discussion.png
- [ ] figure_6_8_creer_groupe.png
- [ ] figure_6_9_notifications.png

### Tests Postman (5 captures):
- [ ] figure_test_1_login.png
- [ ] figure_test_2_create_asset.png
- [ ] figure_test_3_get_alerts.png ⭐
- [ ] figure_test_4_send_message.png
- [ ] figure_test_5_create_group.png

**Total: 25 captures** ✅

---

## 🚀 ORDRE RECOMMANDÉ

1. **Lancez l'application** (backend + frontend)
2. **Créez les alertes de test** (`python3 create_test_alerts.py`)
3. **Prenez les captures** dans l'ordre des sprints
4. **Tests Postman** à la fin
5. **Vérifiez** que toutes les 25 images sont OK

**Temps estimé: 1-2 heures**

---

**Vous êtes prêt à prendre toutes les captures!** 📸

**Bon courage!** 🎯
