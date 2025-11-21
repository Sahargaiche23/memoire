# 📊 DIAGRAMME DE CAS D'UTILISATION GLOBAL

## Vue d'Ensemble

Ce diagramme représente **tous les cas d'utilisation** du système ERP Patrimoine Municipal organisés par acteur.

---

## 🎭 ACTEURS DU SYSTÈME

### 1. **Administrateur** 👑
- Rôle: Gestion complète du système
- Couleur: Rouge (#FF6B6B)
- Responsabilités: Configuration, sécurité, audit

### 2. **Responsable Patrimoine** 💼
- Rôle: Gestion des actifs et maintenances
- Couleur: Turquoise (#4ECDC4)
- Responsabilités: CRUD actifs, planification, rapports

### 3. **Responsable Service** 📋
- Rôle: Suivi des actifs de son service
- Couleur: Bleu (#45B7D1)
- Responsabilités: Consultation, demandes, suivi

### 4. **Agent Maintenance** 🔧
- Rôle: Exécution des maintenances
- Couleur: Orange (#FFA07A)
- Responsabilités: Interventions, mise à jour statuts

### 5. **Auditeur** 📈
- Rôle: Analyse et audit
- Couleur: Vert (#95E1D3)
- Responsabilités: Consultation rapports, export données

---

## 📦 PACKAGES DE CAS D'UTILISATION

### Package 1: Gestion Système (Administrateur)

```
┌─────────────────────────────────────────────────┐
│           GESTION SYSTÈME                       │
├─────────────────────────────────────────────────┤
│ UC01: Gérer les utilisateurs                    │
│ UC02: Gérer les rôles et permissions            │
│ UC03: Gérer les catégories d'actifs             │
│ UC04: Configurer le système                     │
│ UC05: Consulter les logs d'audit                │
└─────────────────────────────────────────────────┘
```

**Détails:**
- **UC01:** Créer, modifier, supprimer, activer/désactiver utilisateurs
- **UC02:** Définir rôles (Admin, RespPatr, RespServ, Agent, Auditeur), assigner permissions
- **UC03:** Créer catégories (mobilier, terrain, véhicule, équipement)
- **UC04:** Paramètres globaux, email, backup, sécurité
- **UC05:** Historique des actions, traçabilité complète

---

### Package 2: Gestion Patrimoine (Responsable Patrimoine)

```
┌─────────────────────────────────────────────────┐
│         GESTION PATRIMOINE                      │
├─────────────────────────────────────────────────┤
│ UC06: Gérer les actifs (CRUD)                   │
│ UC07: Planifier les maintenances                │
│ UC08: Consulter les alertes                     │
│ UC09: Générer des rapports                      │
│ UC10: Enregistrer les mouvements d'actifs       │
└─────────────────────────────────────────────────┘
```

**Détails:**
- **UC06:** Create, Read, Update, Delete actifs avec QR codes
- **UC07:** Planification préventive/corrective, assignation agents
- **UC08:** Alertes intelligentes avec priorités (CRITICAL, HIGH, MEDIUM)
- **UC09:** Rapports PDF avec LaTeX (actifs, maintenances, coûts)
- **UC10:** Traçabilité déplacements (transfert, mise en service, retrait)

**Relations:**
- UC07 **include** UC06 (planifier maintenance nécessite actif existant)
- UC10 **include** UC06 (mouvement nécessite actif existant)

---

### Package 3: Gestion Service (Responsable Service)

```
┌─────────────────────────────────────────────────┐
│          GESTION SERVICE                        │
├─────────────────────────────────────────────────┤
│ UC11: Consulter les actifs de son service       │
│ UC12: Créer une demande de maintenance          │
│ UC13: Suivre les interventions                  │
│ UC14: Communiquer via messagerie                │
└─────────────────────────────────────────────────┘
```

**Détails:**
- **UC11:** Vue filtrée par service, accès lecture seule
- **UC12:** Demande intervention (urgente/planifiée)
- **UC13:** Suivi statut en temps réel
- **UC14:** Communication interne avec agents et admin

**Relations:**
- UC12 **extend** UC07 (demande peut devenir planification)

---

### Package 4: Opérations Maintenance (Agent Maintenance)

```
┌─────────────────────────────────────────────────┐
│       OPÉRATIONS MAINTENANCE                    │
├─────────────────────────────────────────────────┤
│ UC15: Consulter ses maintenances assignées      │
│ UC16: Mettre à jour le statut d'intervention    │
│ UC17: Enregistrer les coûts réels               │
│ UC18: Ajouter des notes techniques              │
└─────────────────────────────────────────────────┘
```

**Détails:**
- **UC15:** Liste des tâches assignées, calendrier
- **UC16:** Statuts: planifié → en_cours → terminé → annulé
- **UC17:** Coûts matériel + main d'œuvre
- **UC18:** Détails techniques, problèmes rencontrés, solutions

**Relations:**
- UC16 **include** UC15 (mise à jour nécessite consultation)
- UC17 **extend** UC16 (coûts optionnels lors MAJ)
- UC18 **extend** UC16 (notes optionnelles lors MAJ)

---

### Package 5: Audit et Analyse (Auditeur)

```
┌─────────────────────────────────────────────────┐
│         AUDIT ET ANALYSE                        │
├─────────────────────────────────────────────────┤
│ UC19: Consulter les rapports                    │
│ UC20: Analyser les statistiques                 │
│ UC21: Exporter les données                      │
└─────────────────────────────────────────────────┘
```

**Détails:**
- **UC19:** Accès à tous les rapports générés
- **UC20:** Tableaux de bord, graphiques, KPIs
- **UC21:** Export CSV, Excel, PDF

---

### Package 6: Fonctionnalités Transversales (Tous)

```
┌─────────────────────────────────────────────────┐
│    FONCTIONNALITÉS TRANSVERSALES                │
├─────────────────────────────────────────────────┤
│ UC22: S'authentifier                            │
│ UC23: Consulter le dashboard                    │
│ UC24: Utiliser la messagerie                    │
│ UC25: Consulter les alertes                     │
│ UC26: Gérer son profil                          │
└─────────────────────────────────────────────────┘
```

**Détails:**
- **UC22:** JWT authentication, login/logout sécurisé
- **UC23:** Dashboard personnalisé selon rôle
- **UC24:** Messagerie interne entre utilisateurs
- **UC25:** Système d'alertes automatique (scheduler)
- **UC26:** Modifier email, mot de passe, préférences

**Accès:**
- **UC22:** TOUS les acteurs (obligatoire)
- **UC23:** TOUS les acteurs
- **UC24:** Admin, RespPatr, RespServ, Agent (pas Auditeur)
- **UC25:** TOUS les acteurs (sauf messagerie pour Auditeur)
- **UC26:** TOUS les acteurs

---

## 🔗 RELATIONS ENTRE CAS D'UTILISATION

### Relations **Include** (obligatoire)

```
UC07 (Planifier maintenances) --include--> UC06 (Gérer actifs)
  ↳ Pour planifier une maintenance, un actif doit exister

UC10 (Enregistrer mouvements) --include--> UC06 (Gérer actifs)
  ↳ Pour enregistrer un mouvement, l'actif doit exister

UC16 (Mettre à jour statut) --include--> UC15 (Consulter maintenances)
  ↳ Pour MAJ, agent doit d'abord consulter sa maintenance
```

### Relations **Extend** (optionnel)

```
UC12 (Demande maintenance) --extend--> UC07 (Planifier maintenances)
  ↳ Une demande peut devenir une planification officielle

UC17 (Enregistrer coûts) --extend--> UC16 (Mettre à jour statut)
  ↳ Enregistrer coûts est optionnel lors MAJ statut

UC18 (Ajouter notes) --extend--> UC16 (Mettre à jour statut)
  ↳ Ajouter notes est optionnel lors MAJ statut
```

---

## 📊 MATRICE ACTEURS × CAS D'UTILISATION

| Cas d'Utilisation | Admin | RespPatr | RespServ | Agent | Auditeur |
|-------------------|-------|----------|----------|-------|----------|
| UC01-UC05 (Système) | ✅ | ❌ | ❌ | ❌ | ❌ |
| UC06-UC10 (Patrimoine) | ❌ | ✅ | ❌ | ❌ | ❌ |
| UC11-UC14 (Service) | ❌ | ❌ | ✅ | ❌ | ❌ |
| UC15-UC18 (Maintenance) | ❌ | ❌ | ❌ | ✅ | ❌ |
| UC19-UC21 (Audit) | ❌ | ❌ | ❌ | ❌ | ✅ |
| UC22 (Authentification) | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC23 (Dashboard) | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC24 (Messagerie) | ✅ | ✅ | ✅ | ✅ | ❌ |
| UC25 (Alertes) | ✅ | ✅ | ✅ | ✅ | ✅ |
| UC26 (Profil) | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 FLUX TYPIQUES

### Flux 1: Création Actif et Planification Maintenance

```
[Responsable Patrimoine]
    ↓
(UC22: S'authentifier)
    ↓
(UC06: Créer actif)
    ↓ include
(UC07: Planifier maintenance)
    ↓
(UC08: Consulter alerte générée automatiquement)
```

### Flux 2: Intervention Agent Maintenance

```
[Agent Maintenance]
    ↓
(UC22: S'authentifier)
    ↓
(UC23: Dashboard - voir maintenances assignées)
    ↓
(UC15: Consulter maintenance)
    ↓ include
(UC16: MAJ statut → "en_cours")
    ↓ extend
(UC17: Enregistrer coûts)
    ↓ extend
(UC18: Ajouter notes techniques)
    ↓
(UC16: MAJ statut → "terminé")
```

### Flux 3: Demande Responsable Service

```
[Responsable Service]
    ↓
(UC22: S'authentifier)
    ↓
(UC11: Consulter actifs de son service)
    ↓
(UC12: Créer demande maintenance)
    ↓ extend
(UC07: Validation par RespPatr → Planification)
    ↓
(UC13: Suivre intervention)
```

### Flux 4: Audit Complet

```
[Auditeur]
    ↓
(UC22: S'authentifier)
    ↓
(UC23: Dashboard - KPIs)
    ↓
(UC20: Analyser statistiques)
    ↓
(UC19: Consulter rapports)
    ↓
(UC21: Exporter données pour audit externe)
```

---

## 📈 STATISTIQUES DU SYSTÈME

```
Total Cas d'Utilisation: 26
├─ Gestion Système: 5 UC
├─ Gestion Patrimoine: 5 UC
├─ Gestion Service: 4 UC
├─ Opérations Maintenance: 4 UC
├─ Audit et Analyse: 3 UC
└─ Transversaux: 5 UC

Relations:
├─ Include: 3
└─ Extend: 3

Acteurs: 5
├─ Administrateur: 10 UC accessibles
├─ Responsable Patrimoine: 10 UC accessibles
├─ Responsable Service: 9 UC accessibles
├─ Agent Maintenance: 9 UC accessibles
└─ Auditeur: 8 UC accessibles
```

---

## 🔐 SÉCURITÉ

### Authentification (UC22)

**Obligatoire pour tous:**
- JWT Token
- Expiration: 24h
- Refresh token disponible

### Autorisation par Rôle

**Contrôle d'accès basé sur les rôles (RBAC):**

```python
@app.route('/api/assets', methods=['POST'])
@jwt_required()
@role_required(['admin', 'responsable_patrimoine'])
def create_asset():
    # Seuls Admin et RespPatr peuvent créer actifs
```

---

## 📝 NOTES IMPORTANTES

### Note 1: Authentification
> Point d'entrée obligatoire pour tous les utilisateurs.
> Aucune fonctionnalité accessible sans authentification valide.

### Note 2: Dashboard Personnalisé
> Le tableau de bord s'adapte automatiquement selon le rôle:
> - **Admin:** Stats globales + gestion système
> - **RespPatr:** Actifs + maintenances + alertes
> - **RespServ:** Actifs de son service
> - **Agent:** Ses maintenances assignées
> - **Auditeur:** Rapports + statistiques

### Note 3: Alertes Intelligentes (UC08/UC25)
> Système d'alertes automatique avec:
> - Génération toutes les 5 minutes (scheduler)
> - Priorités: CRITICAL, HIGH, MEDIUM
> - Types: MAINTENANCE_URGENT, MAINTENANCE_LATE, ASSET_MAINTENANCE_REQUIRED
> - Possibilité d'ignorer définitivement (dismissed)

---

## 🎨 GÉNÉRATION DU DIAGRAMME

### Fichier Source
```
diagrammes/use_case_global.puml
```

### Générer l'image PNG

**Méthode 1: PlantUML local**
```bash
cd diagrammes
plantuml use_case_global.puml
```

**Méthode 2: Script Python**
```bash
cd diagrammes
python3 generate_uml.py
```

**Méthode 3: Serveur en ligne**
```
http://www.plantuml.com/plantuml/uml/use_case_global.puml
```

---

## 📚 RÉFÉRENCES

- **Spécifications:** ANALYSE_FONCTIONNELLE.md
- **Diagrammes UML:** DIAGRAMMES_UML_TOUS.md
- **Documentation Alertes:** ALERTES_DISMISSED_SUPPRESSION_DEFINITIVE.md
- **Architecture:** README.md

---

## ✅ VALIDATION

**Ce diagramme couvre:**
- ✅ 5 acteurs distincts
- ✅ 26 cas d'utilisation
- ✅ 6 packages fonctionnels
- ✅ Relations include/extend
- ✅ Sécurité et authentification
- ✅ Cohérence avec le système implémenté

**Conformité:**
- ✅ UML 2.5
- ✅ PlantUML syntax
- ✅ Best practices Use Case diagrams
