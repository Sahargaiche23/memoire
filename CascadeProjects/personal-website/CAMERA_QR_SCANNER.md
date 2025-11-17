# 📷 Scanner QR Code avec Caméra du Téléphone

## 🎯 Vue d'ensemble

Guide pour scanner les codes QR directement avec la caméra de votre téléphone.

---

## 📱 Méthodes de Scanning

### Méthode 1: Scanner Natif du Téléphone

#### iPhone (iOS)
1. Ouvrez l'appareil photo
2. Pointez vers le code QR
3. Une notification apparaît
4. Cliquez sur la notification
5. Vous êtes redirigé vers le lien

#### Android
1. Ouvrez Google Lens
2. Pointez vers le code QR
3. Cliquez sur le lien
4. Vous êtes redirigé

### Méthode 2: Application QR Scanner

#### Télécharger une Application
1. Allez sur l'App Store ou Google Play
2. Cherchez "QR Code Scanner"
3. Téléchargez une application gratuite
4. Ouvrez l'application
5. Scannez le code QR

### Méthode 3: Scanner Web (Recommandé)

**Avantage:** Pas besoin d'application!

---

## 🚀 Utiliser le Scanner Web

### Étape 1: Ouvrir le Scanner
1. Sur votre téléphone, allez à:
   ```
   http://localhost:3000/qr-scanner
   ```
2. Ou scannez ce code QR

### Étape 2: Accorder l'Accès à la Caméra
1. Le navigateur demande l'accès à la caméra
2. Cliquez sur **"Autoriser"**
3. La caméra s'ouvre

### Étape 3: Scanner le Code QR
1. Pointez votre téléphone vers le code QR
2. Attendez que le code soit reconnu
3. Les informations s'affichent automatiquement

### Étape 4: Consulter les Informations
1. Vous verrez les détails de l'actif ou de l'utilisateur
2. Cliquez sur "Imprimer" si nécessaire
3. Cliquez sur "Nouveau Scan" pour scanner un autre code

---

## 🎬 Étapes Détaillées avec Caméra

### Pour Actifs

**Étape 1: Ouvrir le Scanner**
```
http://localhost:3000/qr-scanner
```

**Étape 2: Autoriser la Caméra**
- Cliquez sur "Autoriser"
- La caméra s'ouvre

**Étape 3: Scanner le Code QR de l'Actif**
- Pointez vers le code QR
- Attendez la reconnaissance
- Les détails de l'actif s'affichent

**Étape 4: Voir les Informations**
- Nom de l'actif
- Catégorie
- Localisation
- Valeur
- Description
- Statut

### Pour Utilisateurs

**Étape 1: Ouvrir le Scanner**
```
http://localhost:3000/qr-scanner
```

**Étape 2: Autoriser la Caméra**
- Cliquez sur "Autoriser"
- La caméra s'ouvre

**Étape 3: Scanner le Code QR de l'Utilisateur**
- Pointez vers le code QR (ex: USR001)
- Attendez la reconnaissance
- Les informations de l'utilisateur s'affichent

**Étape 4: Voir les Informations**
- Nom d'utilisateur
- Nom complet
- Email
- Rôle
- Date de création

---

## 🔧 Dépannage Caméra

### La Caméra ne Fonctionne pas

**Problème:** "Caméra non disponible"

**Solutions:**
1. Vérifiez que vous êtes sur HTTPS (ou localhost)
2. Vérifiez les permissions du navigateur
3. Essayez un autre navigateur
4. Redémarrez le téléphone

### Le Code QR n'est pas Reconnu

**Problème:** "Code QR non reconnu"

**Solutions:**
1. Assurez-vous que le code QR est clair
2. Nettoyez la caméra
3. Améliorez l'éclairage
4. Essayez d'autres angles
5. Utilisez la méthode manuelle (entrer le code)

### Pas d'Accès à la Caméra

**Problème:** "Accès à la caméra refusé"

**Solutions:**
1. Allez aux paramètres du navigateur
2. Autorisez l'accès à la caméra
3. Rafraîchissez la page
4. Réessayez

---

## 📋 Codes QR à Tester

### Actifs
- **QR001** - Mairie Centrale
- **QR002** - Centre de Santé
- **QR003** - Bibliothèque Municipale
- **QR004** - Ambulance 001
- **QR005** - Camion Poubelle 001

### Utilisateurs
- **USR001** - Admin
- **USR002** - Responsable Patrimoine
- **USR003** - Agent Maintenance
- **USR004** - Auditeur
- **USR005** - Responsable Service

---

## 🎯 Cas d'Usage Réels

### Cas 1: Technicien sur le Terrain
```
1. Arrive sur site
2. Ouvre le scanner QR sur son téléphone
3. Scanne le code QR de l'actif
4. Voit les informations (localisation, statut)
5. Effectue l'intervention
6. Enregistre le résultat
```

### Cas 2: Identification Rapide
```
1. Rencontre un collègue
2. Ouvre le scanner QR
3. Scanne le code QR du collègue
4. Voit ses informations (nom, rôle, email)
5. Peut le contacter
```

### Cas 3: Vérification d'Inventaire
```
1. Agent d'inventaire arrive
2. Ouvre le scanner QR
3. Scanne chaque actif
4. Vérifie les informations
5. Confirme la présence
6. Enregistre les notes
```

---

## 📱 Navigateurs Supportés

### iOS (iPhone/iPad)
- ✅ Safari
- ✅ Chrome
- ✅ Firefox
- ✅ Edge

### Android
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Samsung Internet

---

## 🔐 Sécurité

### Données Affichées
- ✅ Informations publiques uniquement
- ✅ Pas de mot de passe
- ✅ Pas de données sensibles
- ✅ Pas de données financières

### Accès à la Caméra
- ✅ Vous contrôlez l'accès
- ✅ Vous pouvez refuser
- ✅ Vous pouvez révoquer
- ✅ Pas de stockage de vidéo

---

## ✅ Checklist

- [ ] Scanner QR accessible
- [ ] Caméra autorisée
- [ ] Caméra fonctionne
- [ ] Code QR reconnu
- [ ] Informations affichées
- [ ] Impression fonctionne
- [ ] Nouveau Scan fonctionne
- [ ] Accès public confirmé

---

## 📞 Support

Pour plus d'informations:
- Consultez `QR_SCANNER_GUIDE.md`
- Consultez `USER_QR_GUIDE.md`
- Consultez `HOW_TO_CREATE_QR.md`

---

**Bon scanning! 📷**

**Dernière mise à jour**: Novembre 2024
