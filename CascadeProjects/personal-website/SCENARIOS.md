# 🎬 Scénarios Détaillés d'Utilisation

## Table des matières
1. [Scénario 1: Gestion d'un nouvel actif](#scénario-1-gestion-dun-nouvel-actif)
2. [Scénario 2: Cycle de maintenance](#scénario-2-cycle-de-maintenance)
3. [Scénario 3: Audit et rapports](#scénario-3-audit-et-rapports)
4. [Scénario 4: Gestion multi-services](#scénario-4-gestion-multi-services)
5. [Scénario 5: Déclassement d'actif](#scénario-5-déclassement-dactif)

---

## Scénario 1: Gestion d'un nouvel actif

### Contexte
La municipalité acquiert une nouvelle ambulance pour le centre de santé. Il faut l'enregistrer dans le système et planifier sa première maintenance.

### Acteurs
- **Responsable du Patrimoine**: Enregistre l'actif
- **Agent de Maintenance**: Planifie la maintenance

### Étapes détaillées

#### Phase 1: Enregistrement de l'ambulance

**Utilisateur**: Responsable du Patrimoine  
**Temps**: 5 minutes

1. **Connexion**
   ```
   URL: http://localhost:3000
   Utilisateur: responsable
   Mot de passe: pass123
   ```

2. **Navigation**
   - Cliquez sur "Actifs" dans la barre de navigation
   - Cliquez sur le bouton "+ Ajouter un actif"

3. **Remplissage du formulaire**
   ```
   Nom: Ambulance Mercedes Sprinter 2024
   Catégorie: Véhicule
   Description: Ambulance de transport sanitaire, équipée de matériel médical
   Date d'acquisition: 2024-11-13
   Valeur d'acquisition: 95000 DT
   Valeur actuelle: 95000 DT
   Localisation: Centre de Santé - Quartier Ouest
   Statut: Actif
   Assigné à: Dr. Fatima Zahra
   ```

4. **Validation**
   - Cliquez sur "Créer"
   - Vérifiez que l'ambulance apparaît dans la liste

5. **Résultat**
   ✅ L'ambulance est enregistrée avec ID (noté pour la maintenance)

#### Phase 2: Planification de la maintenance initiale

**Utilisateur**: Agent de Maintenance  
**Temps**: 3 minutes

1. **Connexion**
   ```
   Utilisateur: agent
   Mot de passe: pass123
   ```

2. **Navigation**
   - Cliquez sur "Maintenance"
   - Cliquez sur "+ Planifier une maintenance"

3. **Remplissage du formulaire**
   ```
   Actif: Ambulance Mercedes Sprinter 2024
   Type: Préventive
   Date prévue: 2024-12-13 (1 mois après acquisition)
   Description: Révision initiale, vérification des systèmes de sécurité
   Coût estimé: 2500 DT
   Statut: Planifiée
   ```

4. **Validation**
   - Cliquez sur "Créer"

5. **Résultat**
   ✅ La maintenance est planifiée

#### Phase 3: Suivi dans le tableau de bord

**Utilisateur**: Responsable du Patrimoine  
**Temps**: 1 minute

1. **Accédez au Tableau de Bord**
2. **Vérifications**
   - Le nombre total d'actifs a augmenté
   - La valeur totale du patrimoine a augmenté de 95000 DT
   - Une alerte de maintenance apparaît

---

## Scénario 2: Cycle de maintenance

### Contexte
Une ambulance a besoin d'une révision complète. Suivre le cycle complet de la maintenance.

### Acteurs
- **Responsable du Patrimoine**: Planifie
- **Agent de Maintenance**: Exécute
- **Auditeur**: Valide

### Étapes détaillées

#### Phase 1: Planification (Responsable)

1. **Accédez à Maintenance**
2. **Créez une maintenance**
   ```
   Actif: Ambulance 001
   Type: Préventive
   Date prévue: 2024-12-01
   Description: Révision moteur, changement d'huile, inspection générale
   Coût estimé: 3500 DT
   Statut: Planifiée
   ```

#### Phase 2: Exécution (Agent)

1. **Connexion en tant qu'Agent**
2. **Accédez à Maintenance**
3. **Modifiez la maintenance**
   - Cliquez sur l'icône ✏️
   - Changez le statut à "En cours"
   - Cliquez "Mettre à jour"

4. **Après l'intervention**
   - Cliquez à nouveau sur ✏️
   - Changez le statut à "Complétée"
   - Entrez la date de complétion: 2024-12-01
   - Mettez à jour le coût réel: 3400 DT (moins que prévu)
   - Cliquez "Mettre à jour"

#### Phase 3: Audit (Auditeur)

1. **Connexion en tant qu'Auditeur**
2. **Accédez à Rapports**
3. **Consultez le tableau "Rapport des Maintenances"**
   - Vérifiez que la maintenance apparaît comme "Complétée"
   - Vérifiez le coût réel

#### Phase 4: Suivi (Responsable)

1. **Accédez au Tableau de Bord**
2. **Vérifiez**
   - L'alerte de maintenance a disparu
   - Le statut de l'ambulance est toujours "Actif"

---

## Scénario 3: Audit et rapports

### Contexte
L'auditeur municipal doit générer un rapport complet du patrimoine pour le conseil municipal.

### Acteur
- **Auditeur**: Génère les rapports

### Étapes détaillées

#### Phase 1: Accès aux rapports

1. **Connexion**
   ```
   Utilisateur: auditeur
   Mot de passe: pass123
   ```

2. **Navigation**
   - Cliquez sur "Rapports"

#### Phase 2: Consultation des statistiques

Vous verrez:
```
Total des Actifs: 12
Actifs Actifs: 11
Valeur Totale: 2,500,000 DT

Distribution par Catégorie:
- Bâtiments: 3
- Véhicules: 3
- Équipements: 3
- Mobilier: 2
- Terrains: 2
```

#### Phase 3: Génération du rapport PDF

1. **Cliquez sur "Exporter en PDF"**
2. **Le fichier se télécharge**
3. **Ouvrez le fichier**
   - Contient les statistiques complètes
   - Liste détaillée de tous les actifs
   - Historique des maintenances

#### Phase 4: Génération du rapport CSV

1. **Cliquez sur "Exporter en CSV"**
2. **Le fichier se télécharge**
3. **Ouvrez dans Excel**
   - Données structurées pour analyse
   - Peut être importé dans d'autres systèmes
   - Facilite les calculs et graphiques

#### Phase 5: Présentation au conseil

- Utilisez le rapport PDF pour la présentation
- Utilisez les données CSV pour les analyses détaillées

---

## Scénario 4: Gestion multi-services

### Contexte
Un véhicule doit être transféré du Service de Santé au Service des Travaux Publics.

### Acteurs
- **Responsable Service (Santé)**: Demande le transfert
- **Responsable Patrimoine**: Approuve et enregistre
- **Responsable Service (TP)**: Reçoit le véhicule

### Étapes détaillées

#### Phase 1: Demande de transfert

**Utilisateur**: Responsable Service (Santé)

1. **Accédez à Actifs**
2. **Trouvez le véhicule**: "Camion Poubelle 001"
3. **Cliquez sur ✏️**
4. **Modifiez**
   ```
   Localisation: Garage Municipal (en transit)
   Assigné à: En attente de Service TP
   ```
5. **Cliquez "Mettre à jour"**

#### Phase 2: Enregistrement du mouvement

**Utilisateur**: Responsable Patrimoine

1. **Accédez à Actifs**
2. **Trouvez le véhicule**
3. **Cliquez sur ✏️**
4. **Modifiez**
   ```
   Localisation: Service des Travaux Publics
   Assigné à: Chef Service TP - Omar Saïd
   ```
5. **Cliquez "Mettre à jour"**

#### Phase 3: Vérification du mouvement

**Utilisateur**: Responsable Patrimoine

1. **Accédez à Rapports**
2. **Consultez le tableau "Liste Complète des Actifs"**
3. **Vérifiez que le véhicule est maintenant assigné à Service TP**

#### Phase 4: Confirmation de réception

**Utilisateur**: Responsable Service (TP)

1. **Accédez à Actifs**
2. **Vérifiez que le véhicule apparaît dans la liste**
3. **Confirmez la réception**

---

## Scénario 5: Déclassement d'actif

### Contexte
Un équipement informatique est obsolète et doit être déclassé du patrimoine.

### Acteurs
- **Responsable Patrimoine**: Effectue le déclassement
- **Auditeur**: Valide

### Étapes détaillées

#### Phase 1: Identification de l'actif

**Utilisateur**: Responsable Patrimoine

1. **Accédez à Actifs**
2. **Recherchez**: "Serveur Informatique"
3. **Consultez les détails**
   ```
   Valeur actuelle: 18,000 DT
   Statut: Actif
   ```

#### Phase 2: Déclassement

1. **Cliquez sur ✏️**
2. **Modifiez**
   ```
   Statut: Déclassé
   Valeur actuelle: 0 DT
   ```
3. **Cliquez "Mettre à jour"**

#### Phase 3: Vérification dans les rapports

**Utilisateur**: Auditeur

1. **Accédez à Rapports**
2. **Consultez les statistiques**
   ```
   Valeur totale réduite de 18,000 DT
   Nombre d'actifs actifs réduit de 1
   ```

#### Phase 4: Documentation

1. **Accédez à Rapports**
2. **Exportez en PDF**
3. **Archivez le rapport**

---

## Scénarios Additionnels

### Scénario 6: Gestion des utilisateurs

**Contexte**: Ajouter un nouvel agent de maintenance

**Utilisateur**: Admin

1. **Accédez à Utilisateurs**
2. **Cliquez "+ Ajouter un utilisateur"**
3. **Remplissez**
   ```
   Nom d'utilisateur: hassan_ali
   Email: hassan@municipality.tn
   Mot de passe: SecurePass2024!
   Nom complet: Hassan Ali Mohamed
   Rôle: Agent Maintenance
   ```
4. **Cliquez "Créer"**
5. **Le nouvel agent peut se connecter**

---

### Scénario 7: Alertes et notifications

**Contexte**: Recevoir et gérer les alertes

**Utilisateur**: Responsable Patrimoine

1. **Accédez au Tableau de Bord**
2. **Consultez la section "Alertes Récentes"**
3. **Vous verrez**
   ```
   - Maintenance urgente requise
   - Maintenance préventive prévue
   - Valeur résiduelle faible
   ```
4. **Cliquez sur une alerte pour la marquer comme lue**

---

## Bonnes Pratiques par Rôle

### Admin
- ✅ Créer les comptes utilisateurs
- ✅ Gérer les rôles et permissions
- ✅ Superviser les opérations
- ❌ Ne pas modifier directement les actifs

### Responsable Patrimoine
- ✅ Enregistrer les nouveaux actifs
- ✅ Planifier les maintenances
- ✅ Générer les rapports
- ✅ Approuver les transferts
- ❌ Ne pas supprimer les données sans archivage

### Agent Maintenance
- ✅ Exécuter les maintenances
- ✅ Enregistrer les interventions
- ✅ Consulter les actifs assignés
- ❌ Ne pas modifier les données d'acquisition

### Auditeur
- ✅ Consulter les rapports
- ✅ Analyser les données
- ✅ Générer les statistiques
- ❌ Ne pas modifier les données

### Responsable Service
- ✅ Consulter les actifs
- ✅ Demander des transferts
- ✅ Signaler les problèmes
- ❌ Ne pas supprimer les actifs

---

**Fin des scénarios détaillés**
