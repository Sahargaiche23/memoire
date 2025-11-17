# 👥 Gestion des Rôles et Accès

## Vue d'ensemble

Le système dispose d'un système complet de gestion des rôles avec contrôle d'accès basé sur les rôles (RBAC).

---

## 🔐 Les 5 Rôles

### 1️⃣ Admin (Administrateur)
**Couleur**: Bleu (#667eea)

**Permissions**:
- ✅ Accès complet au système
- ✅ Gestion des utilisateurs (créer, modifier, supprimer)
- ✅ Gestion des actifs (créer, modifier, supprimer)
- ✅ Gestion des maintenances (créer, modifier, supprimer)
- ✅ Génération de rapports
- ✅ Export de données
- ✅ Gestion des mouvements
- ✅ Consultation des alertes

**Pages accessibles**:
- Tableau de bord
- Actifs
- Maintenance
- Utilisateurs
- Rapports

**Cas d'usage**:
- Administrateur système
- Superviseur général
- Gestionnaire de configuration

---

### 2️⃣ Responsable Patrimoine
**Couleur**: Violet (#764ba2)

**Permissions**:
- ✅ Gestion complète des actifs
- ✅ Planification des maintenances
- ✅ Modification des maintenances
- ✅ Génération de rapports
- ✅ Export de données
- ✅ Gestion des mouvements
- ✅ Consultation des alertes
- ❌ Pas de gestion des utilisateurs

**Pages accessibles**:
- Tableau de bord
- Actifs
- Maintenance
- Rapports

**Cas d'usage**:
- Chef du service patrimoine
- Superviseur des actifs
- Responsable de l'inventaire

---

### 3️⃣ Responsable Service
**Couleur**: Rose (#f093fb)

**Permissions**:
- ✅ Consultation des actifs
- ✅ Consultation des maintenances
- ✅ Demande de mouvements
- ✅ Consultation des alertes
- ❌ Pas de création d'actifs
- ❌ Pas de planification de maintenance
- ❌ Pas de gestion des utilisateurs

**Pages accessibles**:
- Tableau de bord
- Actifs (consultation)
- Maintenance (consultation)

**Cas d'usage**:
- Chef de service municipal
- Responsable de département
- Demandeur de transferts

---

### 4️⃣ Agent Maintenance
**Couleur**: Cyan (#4facfe)

**Permissions**:
- ✅ Consultation des actifs
- ✅ Consultation des maintenances
- ✅ Enregistrement des interventions
- ✅ Consultation des alertes
- ❌ Pas de création d'actifs
- ❌ Pas de planification de maintenance
- ❌ Pas de gestion des utilisateurs

**Pages accessibles**:
- Tableau de bord
- Maintenance

**Cas d'usage**:
- Technicien de maintenance
- Ouvrier spécialisé
- Intervenant terrain

---

### 5️⃣ Auditeur
**Couleur**: Vert (#43e97b)

**Permissions**:
- ✅ Consultation des actifs
- ✅ Consultation des maintenances
- ✅ Génération de rapports
- ✅ Export de données
- ✅ Consultation des alertes
- ❌ Pas de modification d'actifs
- ❌ Pas de création de maintenances
- ❌ Pas de gestion des utilisateurs

**Pages accessibles**:
- Tableau de bord
- Actifs (consultation)
- Rapports

**Cas d'usage**:
- Auditeur financier
- Contrôleur de gestion
- Inspecteur municipal

---

## 📋 Matrice des Permissions

| Permission | Admin | Resp. Patrimoine | Resp. Service | Agent Maint. | Auditeur |
|-----------|-------|------------------|---------------|--------------|----------|
| Voir Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ |
| Voir Actifs | ✅ | ✅ | ✅ | ✅ | ✅ |
| Créer Actif | ✅ | ✅ | ❌ | ❌ | ❌ |
| Modifier Actif | ✅ | ✅ | ❌ | ❌ | ❌ |
| Supprimer Actif | ✅ | ❌ | ❌ | ❌ | ❌ |
| Voir Maintenance | ✅ | ✅ | ✅ | ✅ | ✅ |
| Créer Maintenance | ✅ | ✅ | ❌ | ❌ | ❌ |
| Modifier Maintenance | ✅ | ✅ | ❌ | ✅ | ❌ |
| Supprimer Maintenance | ✅ | ❌ | ❌ | ❌ | ❌ |
| Voir Utilisateurs | ✅ | ❌ | ❌ | ❌ | ❌ |
| Gérer Utilisateurs | ✅ | ❌ | ❌ | ❌ | ❌ |
| Voir Rapports | ✅ | ✅ | ❌ | ❌ | ✅ |
| Exporter Rapports | ✅ | ✅ | ❌ | ❌ | ✅ |
| Gérer Mouvements | ✅ | ✅ | ✅ | ❌ | ❌ |
| Voir Alertes | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 👨‍💼 Créer des Utilisateurs (Admin)

### Étape 1: Accédez à la Gestion des Utilisateurs
1. Connectez-vous en tant qu'**admin**
2. Cliquez sur **"Utilisateurs"** dans la navigation

### Étape 2: Créer un Nouvel Utilisateur
1. Cliquez sur **"+ Ajouter un utilisateur"**
2. Remplissez le formulaire:

```
Nom d'utilisateur: ali_ben_123
Email: ali@municipality.tn
Mot de passe: SecurePass2024!
Nom complet: Ali Ben Ahmed
Rôle: Responsable Patrimoine
```

### Étape 3: Sélectionner le Rôle
Choisissez parmi:
- Admin
- Responsable Patrimoine
- Responsable Service
- Agent Maintenance
- Auditeur

### Étape 4: Créer
1. Cliquez sur **"Créer"**
2. L'utilisateur est créé et peut se connecter

---

## 🎯 Scénarios d'Attribution de Rôles

### Scénario 1: Nouvelle Municipalité
```
1 Admin (Gestionnaire IT)
1 Responsable Patrimoine (Chef service patrimoine)
2 Agents Maintenance (Techniciens)
1 Auditeur (Contrôleur financier)
```

### Scénario 2: Petite Municipalité
```
1 Admin (Gestionnaire IT)
1 Responsable Patrimoine (Cumule plusieurs fonctions)
1 Agent Maintenance (Technicien)
```

### Scénario 3: Grande Municipalité
```
1 Admin (Gestionnaire IT)
2 Responsables Patrimoine (Superviseurs)
3 Responsables Service (Chefs de service)
5 Agents Maintenance (Techniciens)
2 Auditeurs (Contrôleurs)
```

---

## 🔄 Modification des Rôles

### Modifier le Rôle d'un Utilisateur
1. Allez à **"Utilisateurs"**
2. Trouvez l'utilisateur
3. Cliquez sur **✏️ (Éditer)**
4. Changez le rôle
5. Cliquez sur **"Mettre à jour"**

### Supprimer un Utilisateur
1. Allez à **"Utilisateurs"**
2. Trouvez l'utilisateur
3. Cliquez sur **🗑️ (Supprimer)**
4. Confirmez la suppression

---

## 🔐 Bonnes Pratiques de Sécurité

### Lors de la Création d'Utilisateurs
- ✅ Utilisez des mots de passe forts (min 8 caractères)
- ✅ Attribuez le rôle minimum nécessaire
- ✅ Utilisez des emails uniques
- ✅ Documentez les attributions de rôles

### Gestion des Accès
- ✅ Révisez régulièrement les rôles
- ✅ Supprimez les comptes inutilisés
- ✅ Changez les mots de passe régulièrement
- ✅ Limitez le nombre d'admins

### Audit
- ✅ Conservez un registre des utilisateurs
- ✅ Documentez les changements de rôles
- ✅ Consultez les logs d'accès
- ✅ Effectuez des audits réguliers

---

## 📊 Interface Adaptée par Rôle

### Admin voit:
```
Navigation: Tableau de bord | Actifs | Maintenance | Utilisateurs | Rapports
```

### Responsable Patrimoine voit:
```
Navigation: Tableau de bord | Actifs | Maintenance | Rapports
```

### Responsable Service voit:
```
Navigation: Tableau de bord | Actifs | Maintenance
```

### Agent Maintenance voit:
```
Navigation: Tableau de bord | Maintenance
```

### Auditeur voit:
```
Navigation: Tableau de bord | Actifs | Rapports
```

---

## 🔧 Implémentation Technique

### Fichier de Configuration des Rôles
```
frontend/src/utils/roleAccess.js
```

Contient:
- Définition des permissions par rôle
- Fonctions de vérification d'accès
- Informations de rôle (nom, couleur)

### Utilisation dans les Composants
```javascript
import { canAccessPage, hasPermission } from '../utils/roleAccess';

// Vérifier l'accès à une page
if (canAccessPage(userRole, 'assets')) {
  // Afficher la page
}

// Vérifier une permission
if (hasPermission(userRole, 'create_asset')) {
  // Afficher le bouton de création
}
```

---

## 📝 Exemple: Créer 5 Utilisateurs

### Admin
```
Utilisateur: admin
Mot de passe: admin123
Rôle: Admin
Nom: Administrateur Système
```

### Responsable Patrimoine
```
Utilisateur: responsable
Mot de passe: pass123
Rôle: Responsable Patrimoine
Nom: Mohamed Ben Ali
```

### Agent Maintenance
```
Utilisateur: agent
Mot de passe: pass123
Rôle: Agent Maintenance
Nom: Ahmed Khaled
```

### Auditeur
```
Utilisateur: auditeur
Mot de passe: pass123
Rôle: Auditeur
Nom: Fatima Zahra
```

### Responsable Service
```
Utilisateur: service_chief
Mot de passe: pass123
Rôle: Responsable Service
Nom: Omar Saïd
```

---

## ✅ Checklist de Configuration

- [ ] Créer le compte Admin
- [ ] Créer le compte Responsable Patrimoine
- [ ] Créer les comptes Agents Maintenance
- [ ] Créer le compte Auditeur
- [ ] Créer les comptes Responsables Service
- [ ] Tester l'accès pour chaque rôle
- [ ] Vérifier les permissions
- [ ] Documenter les attributions

---

**Dernière mise à jour**: Novembre 2024
