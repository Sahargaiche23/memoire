# 📖 Guide Complet d'Utilisation

## Table des matières
1. [Démarrage rapide](#démarrage-rapide)
2. [Interface utilisateur](#interface-utilisateur)
3. [Workflows principaux](#workflows-principaux)
4. [Conseils et bonnes pratiques](#conseils-et-bonnes-pratiques)

---

## 🚀 Démarrage Rapide

### Première connexion

1. **Ouvrez l'application**: http://localhost:3000
2. **Connectez-vous** avec:
   - **Utilisateur**: `admin`
   - **Mot de passe**: `admin123`

3. **Vous êtes maintenant sur le Tableau de Bord**

### Tableau de Bord - Vue d'ensemble

Le tableau de bord affiche:
- 📊 **4 cartes statistiques** en haut
- 📈 **2 graphiques** au centre (Pie chart et Bar chart)
- 🔔 **Alertes récentes** en bas

---

## 🎨 Interface Utilisateur

### Barre de Navigation

```
[🇹🇳 Patrimoine Municipal] [Tableau de bord] [Actifs] [Maintenance] [Utilisateurs] [Rapports]
                                                                    [Profil] [Déconnexion]
```

### Couleurs et Statuts

| Couleur | Signification |
|---------|---------------|
| 🟢 Vert | Actif / Complété |
| 🟡 Jaune | En attente / En cours |
| 🔴 Rouge | Problème / Suppression |
| 🔵 Bleu | Information |

---

## 📋 Workflows Principaux

### Workflow 1: Ajouter un nouvel actif

**Durée estimée**: 5 minutes

**Étapes:**

1. Cliquez sur **"Actifs"** dans la navigation
2. Cliquez sur le bouton **"+ Ajouter un actif"** (en haut à droite)
3. Remplissez le formulaire:

   ```
   Nom: [Entrez le nom de l'actif]
   Exemple: "Ambulance 001"
   
   Catégorie: [Sélectionnez]
   Options: Bâtiment, Véhicule, Équipement, Mobilier, Terrain
   
   Description: [Optionnel]
   Exemple: "Ambulance Mercedes Sprinter 2020"
   
   Date d'acquisition: [YYYY-MM-DD]
   Exemple: "2020-06-15"
   
   Valeur d'acquisition: [Montant en DT]
   Exemple: "85000"
   
   Valeur actuelle: [Montant en DT]
   Exemple: "65000"
   
   Localisation: [Adresse ou site]
   Exemple: "Centre de santé - Rue de la Paix"
   
   Statut: [Sélectionnez]
   Options: Actif, Maintenance, Hors service, Déclassé
   
   Assigné à: [Responsable]
   Exemple: "Dr. Ahmed Ben Ali"
   ```

4. Cliquez sur **"Créer"**
5. ✅ L'actif apparaît maintenant dans la liste

**Conseils:**
- Utilisez des noms clairs et uniques
- Mettez à jour régulièrement la valeur actuelle
- Assignez toujours un responsable

---

### Workflow 2: Planifier une maintenance préventive

**Durée estimée**: 3 minutes

**Étapes:**

1. Cliquez sur **"Maintenance"** dans la navigation
2. Cliquez sur **"+ Planifier une maintenance"**
3. Remplissez les informations:

   ```
   Actif: [Sélectionnez dans la liste]
   Exemple: "Ambulance 001"
   
   Type de maintenance: [Sélectionnez]
   - Préventive: Maintenance régulière programmée
   - Corrective: Réparation suite à une panne
   
   Date prévue: [YYYY-MM-DD]
   Exemple: "2024-12-15"
   
   Description: [Détails de l'intervention]
   Exemple: "Révision moteur, changement d'huile, inspection générale"
   
   Coût estimé: [Montant en DT]
   Exemple: "3500"
   
   Statut: "Planifiée" (par défaut)
   ```

4. Cliquez sur **"Créer"**
5. ✅ La maintenance est maintenant planifiée

**Exemple de calendrier de maintenance:**

| Actif | Type | Fréquence | Coût estimé |
|-------|------|-----------|------------|
| Ambulance 001 | Préventive | Tous les 6 mois | 3500 DT |
| Bâtiment Mairie | Préventive | Annuelle | 5000 DT |
| Véhicule Service | Corrective | À la demande | Variable |

---

### Workflow 3: Enregistrer une intervention complétée

**Durée estimée**: 2 minutes

**Étapes:**

1. Allez à **"Maintenance"**
2. Trouvez la maintenance à mettre à jour
3. Cliquez sur l'icône **✏️ (Éditer)**
4. Modifiez les champs:

   ```
   Statut: Changez à "En cours"
   (Puis cliquez "Mettre à jour")
   
   Une fois terminée:
   Statut: Changez à "Complétée"
   Coût réel: Entrez le coût final
   Date complétée: [Date d'aujourd'hui]
   ```

5. Cliquez sur **"Mettre à jour"**
6. ✅ L'intervention est enregistrée

---

### Workflow 4: Générer un rapport d'inventaire

**Durée estimée**: 1 minute

**Étapes:**

1. Cliquez sur **"Rapports"** dans la navigation
2. Consultez les statistiques affichées:
   - Total des actifs
   - Actifs actifs
   - Valeur totale du patrimoine
   - Distribution par catégorie

3. Pour exporter:
   - Cliquez sur **"Exporter en PDF"** pour un rapport complet
   - Cliquez sur **"Exporter en CSV"** pour les données brutes

4. ✅ Le fichier est téléchargé automatiquement

**Utilisation des rapports:**
- **PDF**: Présentation, archivage, audit
- **CSV**: Analyse dans Excel, import dans d'autres systèmes

---

### Workflow 5: Gérer les utilisateurs (Admin uniquement)

**Durée estimée**: 5 minutes

**Étapes:**

1. Cliquez sur **"Utilisateurs"** (visible uniquement pour Admin)
2. Cliquez sur **"+ Ajouter un utilisateur"**
3. Remplissez le formulaire:

   ```
   Nom d'utilisateur: [Identifiant unique]
   Exemple: "ali_ben_123"
   
   Email: [Adresse email]
   Exemple: "ali@municipality.tn"
   
   Mot de passe: [Sécurisé, min 8 caractères]
   Exemple: "SecurePass2024!"
   
   Nom complet: [Prénom et nom]
   Exemple: "Ali Ben Ahmed"
   
   Rôle: [Sélectionnez le rôle]
   Options:
   - Admin: Accès complet
   - Responsable Patrimoine: Gestion complète
   - Responsable Service: Consultation et transferts
   - Agent Maintenance: Enregistrement interventions
   - Auditeur: Consultation rapports
   ```

4. Cliquez sur **"Créer"**
5. ✅ L'utilisateur peut maintenant se connecter

**Gestion des utilisateurs existants:**

- **Modifier**: Cliquez sur ✏️, changez le rôle ou l'email
- **Supprimer**: Cliquez sur 🗑️, confirmez

---

## 💡 Conseils et Bonnes Pratiques

### Gestion des Actifs

✅ **À faire:**
- Utiliser des noms descriptifs et uniques
- Mettre à jour régulièrement les valeurs
- Assigner un responsable à chaque actif
- Documenter les modifications importantes

❌ **À éviter:**
- Noms génériques ("Actif 1", "Équipement")
- Laisser les champs vides
- Oublier de mettre à jour le statut
- Dupliquer les actifs

### Maintenance Préventive

✅ **Bonnes pratiques:**
- Planifier 2-3 mois à l'avance
- Documenter l'historique complet
- Estimer les coûts réalistes
- Respecter les calendriers

**Fréquences recommandées:**
- Véhicules: Tous les 6 mois
- Équipements: Annuellement
- Bâtiments: Annuellement
- Mobilier: Tous les 2-3 ans

### Rapports et Audits

✅ **Utilisation optimale:**
- Générer des rapports mensuels
- Archiver les rapports PDF
- Exporter les données pour analyse
- Suivre les tendances de coûts

### Sécurité des Données

✅ **Recommandations:**
- Changer les mots de passe régulièrement
- Ne pas partager les identifiants
- Utiliser des mots de passe forts
- Sauvegarder régulièrement les données

---

## 🎓 Cas d'Usage Avancés

### Cas 1: Transfert d'actif entre services

**Scénario**: Un véhicule doit être transféré du Service de Santé au Service des Travaux Publics

**Étapes:**
1. Allez à **"Actifs"**
2. Trouvez le véhicule
3. Cliquez sur ✏️
4. Modifiez:
   - Localisation: "Service des Travaux Publics"
   - Assigné à: "Chef du Service TP"
5. Cliquez sur "Mettre à jour"
6. ✅ Le transfert est enregistré

### Cas 2: Déclassement d'un actif

**Scénario**: Un équipement est hors d'usage et doit être déclassé

**Étapes:**
1. Allez à **"Actifs"**
2. Trouvez l'équipement
3. Cliquez sur ✏️
4. Changez le statut à **"Déclassé"**
5. Mettez à jour la valeur actuelle à 0
6. Cliquez sur "Mettre à jour"
7. ✅ L'actif est marqué comme déclassé

### Cas 3: Analyse des coûts de maintenance

**Étapes:**
1. Allez à **"Rapports"**
2. Consultez le tableau "Rapport des Maintenances"
3. Exportez en CSV
4. Ouvrez dans Excel pour analyser:
   - Coûts totaux par type
   - Coûts par actif
   - Tendances mensuelles

---

## 📞 FAQ

**Q: Comment réinitialiser mon mot de passe?**
A: Contactez l'administrateur pour réinitialiser votre compte.

**Q: Puis-je modifier un actif après sa création?**
A: Oui, cliquez sur l'icône ✏️ pour modifier.

**Q: Comment supprimer un actif?**
A: Cliquez sur l'icône 🗑️, puis confirmez.

**Q: Où voir l'historique des modifications?**
A: Les modifications sont enregistrées avec la date de création/mise à jour.

**Q: Comment exporter les données?**
A: Allez à "Rapports" et cliquez sur "Exporter en CSV" ou "Exporter en PDF".

---

**Dernière mise à jour**: Novembre 2024
