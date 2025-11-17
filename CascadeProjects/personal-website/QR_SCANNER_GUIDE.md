# 📱 Guide Complet - QR Scanner

## 🎯 Vue d'ensemble

Le QR Scanner permet d'accéder aux informations d'un actif sans authentification, idéal pour les utilisateurs mobiles sur le terrain.

---

## 🚀 Accéder au QR Scanner

### Méthode 1: Lien Direct (Sans Authentification)
```
http://localhost:3000/qr-scanner
```

### Méthode 2: Depuis la Page de Connexion
1. Allez à `http://localhost:3000/login`
2. Cliquez sur le lien "QR Scanner" (si disponible)
3. Vous serez redirigé vers la page de scanner

---

## 📝 Codes QR Disponibles

Les codes QR sont générés automatiquement pour chaque actif. Voici les codes disponibles:

### Bâtiments
- **QR001** - Mairie Centrale
- **QR002** - Centre de Santé
- **QR003** - Bibliothèque Municipale

### Véhicules
- **QR004** - Ambulance 001
- **QR005** - Camion Poubelle 001
- **QR006** - Véhicule de Service 001

### Équipements
- **QR007** - Serveur Informatique
- **QR008** - Système de Climatisation
- **QR009** - Groupe Électrogène

### Mobilier
- **QR010** - Bureau Directeur
- **QR011** - Chaises de Réunion (Lot)

### Terrains
- **QR012** - Terrain Parc Municipal
- **QR013** - Terrain Futur Stade

---

## 🧪 Tester le QR Scanner

### Étape 1: Ouvrir le QR Scanner
```
http://localhost:3000/qr-scanner
```

### Étape 2: Entrer un Code QR
1. Cliquez dans le champ d'entrée
2. Tapez: **QR001**
3. Cliquez sur **"Rechercher"**

### Étape 3: Voir les Détails
Vous devriez voir:
- ✅ Nom: "Mairie Centrale"
- ✅ Catégorie: "bâtiment"
- ✅ Localisation: "Centre-ville, Rue de la Liberté"
- ✅ Valeur d'acquisition: "500000 DT"
- ✅ Valeur actuelle: "450000 DT"
- ✅ Description: "Bâtiment administratif principal"
- ✅ Statut: "Actif"

### Étape 4: Imprimer
1. Cliquez sur **"🖨️ Imprimer"**
2. La page d'impression s'ouvre
3. Appuyez sur Ctrl+P ou utilisez le menu Imprimer

### Étape 5: Nouveau Scan
1. Cliquez sur **"🔄 Nouveau Scan"**
2. Le formulaire est réinitialisé
3. Vous pouvez entrer un nouveau code QR

---

## 🎨 Interface du QR Scanner

### Éléments Principaux

#### En-tête
- 📱 Icône Smartphone
- Titre: "Scanner QR Code"
- Description: "Accédez aux informations d'un actif en scannant son code QR"

#### Formulaire de Saisie
- Champ d'entrée: "Entrez le code QR ou scannez..."
- Bouton: "Rechercher"

#### Affichage des Détails
- Nom de l'actif avec statut
- Grille d'informations (6 colonnes)
- Description complète
- Boutons d'action

#### Boutons d'Action
- 🖨️ Imprimer
- 🔄 Nouveau Scan

---

## 📊 Informations Affichées

Pour chaque actif, vous verrez:

| Information | Exemple |
|-------------|---------|
| **Nom** | Mairie Centrale |
| **Catégorie** | Bâtiment |
| **Localisation** | Centre-ville, Rue de la Liberté |
| **Affecté à** | Mohamed Ben Ali |
| **Date d'Acquisition** | 15/03/2015 |
| **Valeur d'Acquisition** | 500 000 DT |
| **Valeur Actuelle** | 450 000 DT |
| **Description** | Bâtiment administratif principal |
| **Statut** | Actif |

---

## 🔐 Sécurité

### Accès Public
- ✅ Pas d'authentification requise
- ✅ Accessible à tous
- ✅ Idéal pour le terrain

### Données Affichées
- ✅ Informations publiques uniquement
- ✅ Pas de données sensibles
- ✅ Pas de données financières détaillées

### Protection
- ✅ Validation du code QR
- ✅ Gestion d'erreurs
- ✅ Messages d'erreur clairs

---

## 📱 Utilisation Mobile

### Sur Smartphone/Tablette
1. Ouvrez le navigateur
2. Allez à `http://localhost:3000/qr-scanner`
3. Entrez le code QR
4. Consultez les informations
5. Imprimez si nécessaire

### Responsive Design
- ✅ Écran complet adapté
- ✅ Formulaire optimisé
- ✅ Texte lisible
- ✅ Boutons tactiles

---

## 🎯 Cas d'Usage

### Cas 1: Technicien sur le Terrain
```
1. Arrive sur site
2. Ouvre http://localhost:3000/qr-scanner
3. Scanne le QR Code de l'actif
4. Voit les informations (localisation, statut, historique)
5. Effectue l'intervention
6. Enregistre le résultat
```

### Cas 2: Inspection Rapide
```
1. Inspecteur arrive
2. Ouvre le QR Scanner
3. Scanne le code
4. Vérifie l'état de l'actif
5. Prend des photos
6. Enregistre les observations
```

### Cas 3: Vérification d'Inventaire
```
1. Agent d'inventaire arrive
2. Ouvre le QR Scanner
3. Scanne chaque actif
4. Vérifie les informations
5. Confirme la présence
6. Enregistre les notes
```

---

## 🔄 Flux de Données

```
1. Utilisateur entre le code QR
2. Frontend envoie une requête GET
3. Backend cherche l'actif
4. Backend retourne les données
5. Frontend affiche les informations
6. Utilisateur consulte les détails
```

### Endpoint API
```
GET /api/assets/qr/<qr_code>
```

### Réponse Exemple
```json
{
  "id": 1,
  "name": "Mairie Centrale",
  "category": "bâtiment",
  "description": "Bâtiment administratif principal",
  "acquisition_date": "2015-03-15",
  "acquisition_value": 500000,
  "current_value": 450000,
  "location": "Centre-ville, Rue de la Liberté",
  "status": "actif",
  "assigned_to": "Mohamed Ben Ali",
  "qr_code": "QR001",
  "created_at": "2025-11-13T10:00:00"
}
```

---

## ✅ Checklist de Test

- [ ] Page QR Scanner accessible
- [ ] Formulaire d'entrée fonctionne
- [ ] Recherche fonctionne
- [ ] Détails affichés correctement
- [ ] Statut visible
- [ ] Impression fonctionne
- [ ] Nouveau Scan réinitialise
- [ ] Accès public confirmé
- [ ] Responsive sur mobile
- [ ] Messages d'erreur clairs

---

## 🐛 Dépannage

### "Actif non trouvé"
```
1. Vérifiez le code QR
2. Assurez-vous que l'actif existe
3. Vérifiez la base de données
4. Consultez la console (F12)
```

### Page ne charge pas
```
1. Vérifiez que le backend démarre
2. Vérifiez l'URL
3. Rafraîchissez la page
4. Consultez la console (F12)
```

### Impression ne fonctionne pas
```
1. Vérifiez les paramètres d'impression
2. Essayez Ctrl+P
3. Vérifiez le navigateur
4. Essayez un autre navigateur
```

---

## 📞 Support

Pour plus d'informations:
- Consultez `TEST_NEW_FEATURES.md`
- Consultez `NEW_FEATURES.md`
- Consultez `GUIDE_UTILISATION.md`

---

**Bon scanning! 📱**

**Dernière mise à jour**: Novembre 2024
