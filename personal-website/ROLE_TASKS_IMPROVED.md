# 🎯 Tâches Améliorées par Rôle

## Vue d'ensemble

Chaque rôle dispose maintenant de tâches améliorées avec support chatbot et messagerie.

---

## 👨‍💼 1. Administrateur Système

### Tâches Principales

#### Gestion des Utilisateurs
```
1. Créer un nouvel utilisateur
   - Aller à: Utilisateurs → + Ajouter un utilisateur
   - Remplir: Username, Email, Mot de passe, Rôle
   - Confirmer: Créer
   
2. Modifier un utilisateur
   - Aller à: Utilisateurs
   - Cliquer: ✏️ (Éditer)
   - Modifier: Les données
   - Confirmer: Mettre à jour
   
3. Supprimer un utilisateur
   - Aller à: Utilisateurs
   - Cliquer: 🗑️ (Supprimer)
   - Confirmer: Suppression
```

#### Gestion des Rôles
```
1. Assigner un rôle
   - Lors de la création d'utilisateur
   - Choisir parmi: Admin, Resp. Patrimoine, Resp. Service, Agent Maintenance, Auditeur
   
2. Modifier les permissions
   - Consulter: ROLE_MANAGEMENT.md
   - Adapter: Les permissions selon les besoins
```

#### Communication
```
1. Envoyer un message
   - Aller à: Messagerie
   - Cliquer: + Nouveau message
   - Sélectionner: Destinataire
   - Écrire: Le message
   - Envoyer: Confirmer
   
2. Utiliser le Chatbot
   - Ouvrir: Chatbot (icône 🤖)
   - Taper: Votre question
   - Exemples: "utilisateur", "rôle", "permission"
```

### Nouvelles Fonctionnalités
- ✅ Messagerie avec les autres admins
- ✅ Chatbot pour l'aide sur la gestion
- ✅ Accès aux informations mobiles

### Endpoints Utiles
```
POST /api/auth/register - Créer un utilisateur
PUT /api/users/<id> - Modifier un utilisateur
DELETE /api/users/<id> - Supprimer un utilisateur
POST /api/messages - Envoyer un message
POST /api/chatbot - Utiliser le chatbot
```

---

## 👨‍💼 2. Responsable Patrimoine

### Tâches Principales

#### Gestion des Actifs
```
1. Créer un actif
   - Aller à: Actifs → + Ajouter un actif
   - Remplir: Nom, Catégorie, Description, Valeur
   - Confirmer: Créer
   
2. Modifier un actif
   - Aller à: Actifs
   - Cliquer: ✏️ (Éditer)
   - Modifier: Les données
   - Confirmer: Mettre à jour
   
3. Supprimer un actif
   - Aller à: Actifs
   - Cliquer: 🗑️ (Supprimer)
   - Confirmer: Suppression
   
4. Générer QR Code
   - Lors de la création d'actif
   - Le QR Code est généré automatiquement
   - Imprimer: Pour étiquetage
```

#### Gestion des Maintenances
```
1. Planifier une maintenance
   - Aller à: Maintenance → + Planifier
   - Sélectionner: Actif
   - Choisir: Type (Préventive/Corrective)
   - Fixer: Date et coût
   - Confirmer: Créer
   
2. Suivre une maintenance
   - Aller à: Maintenance
   - Voir: Statut (Planifiée/En cours/Complétée)
   - Mettre à jour: Le statut
```

#### Gestion des Mouvements
```
1. Enregistrer un mouvement
   - Aller à: Mouvements → + Nouveau mouvement
   - Sélectionner: Actif
   - Indiquer: De/Vers (localisation)
   - Ajouter: Raison
   - Confirmer: Enregistrer
```

#### Génération de Rapports
```
1. Générer un rapport
   - Aller à: Rapports
   - Choisir: Type de rapport
   - Sélectionner: Paramètres (Période, Catégorie)
   - Générer: PDF ou Excel
   - Télécharger: Le fichier
```

#### Communication
```
1. Envoyer un message
   - Aller à: Messagerie
   - Cliquer: + Nouveau message
   - Sélectionner: Responsable de service ou Agent
   - Écrire: Le message
   - Envoyer: Confirmer
   
2. Utiliser le Chatbot
   - Ouvrir: Chatbot (icône 🤖)
   - Taper: Votre question
   - Exemples: "actif", "maintenance", "rapport"
```

### Nouvelles Fonctionnalités
- ✅ Messagerie avec les responsables de service
- ✅ Chatbot pour l'aide sur la gestion des actifs
- ✅ Accès aux informations mobiles des actifs

### Endpoints Utiles
```
POST /api/assets - Créer un actif
PUT /api/assets/<id> - Modifier un actif
GET /api/assets - Récupérer les actifs
POST /api/maintenances - Planifier une maintenance
POST /api/movements - Enregistrer un mouvement
POST /api/messages - Envoyer un message
POST /api/chatbot - Utiliser le chatbot
```

---

## 👨‍💼 3. Responsable de Service

### Tâches Principales

#### Consultation des Actifs
```
1. Voir les actifs du service
   - Aller à: Actifs
   - Voir: Liste des actifs affectés
   - Cliquer: Sur un actif pour les détails
```

#### Demande de Mouvements
```
1. Demander un transfert d'actif
   - Aller à: Mouvements → + Nouveau mouvement
   - Sélectionner: Actif
   - Indiquer: Destination
   - Ajouter: Raison
   - Envoyer: La demande
   
2. Suivre la demande
   - Aller à: Mouvements
   - Voir: Statut de la demande
   - Attendre: Approbation du responsable patrimoine
```

#### Demande de Maintenance
```
1. Demander une maintenance
   - Aller à: Maintenance
   - Cliquer: + Demander une maintenance
   - Sélectionner: Actif
   - Décrire: Le problème
   - Envoyer: La demande
```

#### Communication
```
1. Envoyer un message
   - Aller à: Messagerie
   - Cliquer: + Nouveau message
   - Sélectionner: Responsable patrimoine
   - Écrire: Le message
   - Envoyer: Confirmer
   
2. Utiliser le Chatbot
   - Ouvrir: Chatbot (icône 🤖)
   - Taper: Votre question
   - Exemples: "mouvement", "maintenance", "demande"
```

### Nouvelles Fonctionnalités
- ✅ Messagerie avec le responsable patrimoine
- ✅ Chatbot pour l'aide sur les demandes
- ✅ Accès aux informations mobiles des actifs

### Endpoints Utiles
```
GET /api/assets - Voir les actifs
POST /api/movements - Demander un mouvement
POST /api/maintenances - Demander une maintenance
POST /api/messages - Envoyer un message
POST /api/chatbot - Utiliser le chatbot
```

---

## 🔧 4. Agent de Maintenance

### Tâches Principales

#### Consultation des Maintenances
```
1. Voir les maintenances planifiées
   - Aller à: Maintenance
   - Voir: Liste des maintenances
   - Cliquer: Sur une maintenance pour les détails
```

#### Enregistrement des Interventions
```
1. Enregistrer une intervention
   - Aller à: Maintenance
   - Cliquer: Sur la maintenance
   - Cliquer: Enregistrer l'intervention
   - Remplir: Détails (Date, Coût, Pièces, Notes)
   - Confirmer: Enregistrer
   
2. Mettre à jour le statut
   - Aller à: Maintenance
   - Cliquer: Sur la maintenance
   - Changer: Statut (En cours → Complétée)
   - Confirmer: Mise à jour
```

#### Accès Mobile
```
1. Scanner un QR Code
   - Ouvrir: L'application mobile
   - Cliquer: Scanner QR Code
   - Pointer: Vers le QR Code de l'actif
   - Voir: Les informations de l'actif
   - Effectuer: L'intervention
   - Enregistrer: Le résultat
```

#### Communication
```
1. Envoyer un message
   - Aller à: Messagerie
   - Cliquer: + Nouveau message
   - Sélectionner: Responsable patrimoine
   - Écrire: Le message
   - Envoyer: Confirmer
   
2. Utiliser le Chatbot
   - Ouvrir: Chatbot (icône 🤖)
   - Taper: Votre question
   - Exemples: "intervention", "maintenance", "aide"
```

### Nouvelles Fonctionnalités
- ✅ Messagerie avec le responsable patrimoine
- ✅ Chatbot pour l'aide sur les interventions
- ✅ Accès mobile via QR Code (sans authentification)

### Endpoints Utiles
```
GET /api/maintenances - Voir les maintenances
PUT /api/maintenances/<id> - Mettre à jour une maintenance
GET /api/assets/qr/<qr_code> - Scanner un QR Code
POST /api/messages - Envoyer un message
POST /api/chatbot - Utiliser le chatbot
```

---

## 📊 5. Auditeur / Contrôleur

### Tâches Principales

#### Consultation des Rapports
```
1. Voir les rapports
   - Aller à: Rapports
   - Voir: Liste des rapports disponibles
   - Cliquer: Sur un rapport pour les détails
```

#### Génération de Rapports
```
1. Générer un rapport personnalisé
   - Aller à: Rapports → + Générer un rapport
   - Choisir: Type (Inventaire, Maintenance, Valeur)
   - Sélectionner: Paramètres (Période, Catégorie)
   - Générer: PDF ou Excel
   - Télécharger: Le fichier
```

#### Consultation des Statistiques
```
1. Voir les statistiques
   - Aller à: Tableau de Bord
   - Voir: Graphiques et statistiques
   - Analyser: Les données
```

#### Consultation des Alertes
```
1. Voir les alertes
   - Aller à: Tableau de Bord
   - Voir: Alertes récentes
   - Cliquer: Sur une alerte pour les détails
```

#### Communication
```
1. Envoyer un message
   - Aller à: Messagerie
   - Cliquer: + Nouveau message
   - Sélectionner: Responsable patrimoine
   - Écrire: Le message
   - Envoyer: Confirmer
   
2. Utiliser le Chatbot
   - Ouvrir: Chatbot (icône 🤖)
   - Taper: Votre question
   - Exemples: "rapport", "statistique", "aide"
```

### Nouvelles Fonctionnalités
- ✅ Messagerie avec le responsable patrimoine
- ✅ Chatbot pour l'aide sur les rapports
- ✅ Accès aux informations mobiles des actifs

### Endpoints Utiles
```
GET /api/statistics - Voir les statistiques
GET /api/alerts - Voir les alertes
GET /api/assets - Voir les actifs
POST /api/messages - Envoyer un message
POST /api/chatbot - Utiliser le chatbot
```

---

## 📱 6. Utilisateur Mobile (Terrain)

### Tâches Principales

#### Scanner un QR Code
```
1. Accéder à l'application mobile
   - Ouvrir: L'application
   - Aller à: Scanner QR Code
   
2. Scanner le QR Code
   - Pointer: Vers le QR Code de l'actif
   - Attendre: La lecture
   
3. Voir les informations
   - Nom de l'actif
   - Catégorie
   - Description
   - Localisation
   - Statut
   - Affectation
   - Historique
```

#### Effectuer une Intervention
```
1. Scanner le QR Code
   - Voir: Les informations de l'actif
   
2. Effectuer l'intervention
   - Vérifier: L'état de l'actif
   - Prendre: Des photos
   - Noter: Les observations
   
3. Enregistrer le résultat
   - Aller à: Maintenance
   - Enregistrer: L'intervention
   - Ajouter: Détails et photos
```

### Nouvelles Fonctionnalités
- ✅ Accès mobile sans authentification
- ✅ Scanner QR Code
- ✅ Informations détaillées de l'actif

### Endpoints Utiles
```
GET /api/assets/qr/<qr_code> - Récupérer un actif par QR Code
```

---

## 🤖 7. Système (Automatique)

### Tâches Automatiques

#### Génération d'Alertes
```
1. Alerte de maintenance
   - Déclenché: 7 jours avant la date de maintenance
   - Notification: Email/SMS
   - Action: Planifier l'intervention
   
2. Alerte de garantie
   - Déclenché: À l'expiration de la garantie
   - Notification: Email/SMS
   - Action: Vérifier la couverture
   
3. Alerte d'amortissement
   - Déclenché: Quand la valeur est faible
   - Notification: Email/SMS
   - Action: Considérer le déclassement
```

#### Génération de Rapports
```
1. Rapport mensuel
   - Généré: Automatiquement le 1er du mois
   - Contenu: Statistiques du mois
   - Destinataires: Responsable patrimoine, Auditeur
   
2. Rapport d'inventaire
   - Généré: Trimestriellement
   - Contenu: Liste complète des actifs
   - Destinataires: Responsable patrimoine, Auditeur
```

#### Calcul d'Amortissement
```
1. Amortissement automatique
   - Calculé: Mensuellement
   - Formule: Valeur actuelle = Valeur initiale - (Amortissement × Mois)
   - Mise à jour: Automatique
```

---

## 📊 Résumé des Améliorations

| Rôle | Messagerie | Chatbot | Mobile | Tâches |
|------|-----------|---------|--------|--------|
| Admin | ✅ | ✅ | ✅ | 3 |
| Resp. Patrimoine | ✅ | ✅ | ✅ | 5 |
| Resp. Service | ✅ | ✅ | ✅ | 3 |
| Agent Maintenance | ✅ | ✅ | ✅ | 3 |
| Auditeur | ✅ | ✅ | ✅ | 4 |
| Utilisateur Mobile | ❌ | ❌ | ✅ | 2 |
| Système | ❌ | ❌ | ❌ | 3 |

---

## 🎯 Cas d'Usage Améliorés

### Cas 1: Technicien sur le Terrain
```
1. Arrive sur site
2. Scanne le QR Code de l'actif
3. Voit les informations (localisation, statut, historique)
4. Effectue l'intervention
5. Enregistre le résultat dans le système
6. Envoie un message au responsable
```

### Cas 2: Responsable Patrimoine
```
1. Reçoit une demande de mouvement
2. Lit le message du responsable de service
3. Approuve la demande
4. Envoie un message de confirmation
5. Génère un rapport
6. Consulte le chatbot pour l'aide
```

### Cas 3: Admin
```
1. Crée un nouvel utilisateur
2. Assigne un rôle
3. Envoie un message de bienvenue
4. Consulte le chatbot pour l'aide
5. Gère les permissions
```

---

## 📞 Support

Pour plus d'informations:
- Consultez `NEW_FEATURES.md` - Nouvelles fonctionnalités
- Consultez `ROLE_MANAGEMENT.md` - Gestion des rôles
- Consultez `GUIDE_UTILISATION.md` - Guide complet

---

**Dernière mise à jour**: Novembre 2024
