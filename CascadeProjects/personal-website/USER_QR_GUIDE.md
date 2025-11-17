# 👤 Guide Complet - QR Code Utilisateur

## 🎯 Vue d'ensemble

Chaque utilisateur a un code QR unique qui peut être partagé et scanné pour accéder à ses informations.

---

## 📱 Codes QR Utilisateurs

Les codes QR sont **automatiquement créés** pour chaque utilisateur lors de l'initialisation.

| Code QR | Utilisateur | Rôle |
|---------|-------------|------|
| USR001 | admin | Administrateur |
| USR002 | responsable | Responsable Patrimoine |
| USR003 | agent | Agent Maintenance |
| USR004 | auditeur | Auditeur |
| USR005 | service_chief | Responsable Service |

---

## 👤 Accéder à Mon Profil

### Étape 1: Cliquer sur l'Icône Profil
1. Connectez-vous avec vos identifiants
2. Dans la navbar, cliquez sur **👤** (en haut à droite)
3. Vous serez redirigé vers votre profil

### Étape 2: Voir Vos Informations
Vous verrez:
- ✅ Nom d'utilisateur
- ✅ Email
- ✅ Nom complet
- ✅ Rôle
- ✅ Date de création
- ✅ **Votre Code QR**

### Étape 3: Voir Votre QR Code
- Votre code QR s'affiche en grand
- Vous pouvez le télécharger
- Vous pouvez copier le code

---

## 🖼️ Télécharger Votre QR Code

### Étape 1: Aller au Profil
1. Cliquez sur **👤** dans la navbar
2. Allez à la section "Mon Code QR"

### Étape 2: Télécharger
1. Cliquez sur **"📥 Télécharger QR"**
2. L'image QR se télécharge sur votre ordinateur
3. Nom du fichier: `username_qr.png`

### Étape 3: Imprimer
1. Ouvrez l'image téléchargée
2. Imprimez-la
3. Collez-la sur votre badge ou document

---

## 📋 Copier Votre Code QR

### Étape 1: Aller au Profil
1. Cliquez sur **👤** dans la navbar
2. Allez à la section "Mon Code QR"

### Étape 2: Copier le Code
1. Cliquez sur **"📋 Copier Code"**
2. Le code est copié dans le presse-papiers
3. Le bouton devient vert et affiche "Copié!"

### Étape 3: Partager
1. Collez le code dans un email
2. Collez le code dans un message
3. Partagez avec vos collègues

---

## 🧪 Tester Votre QR Code

### Test 1: Scanner Votre Propre Code
1. Allez à `http://localhost:3000/qr-scanner`
2. Entrez votre code QR (ex: **USR001**)
3. Cliquez sur "Rechercher"
4. Vous verrez vos informations

### Test 2: Partager Avec un Collègue
1. Téléchargez votre QR code
2. Partagez l'image avec un collègue
3. Votre collègue va à `http://localhost:3000/qr-scanner`
4. Il entre votre code QR
5. Il voit vos informations

### Test 3: Copier et Partager le Code
1. Allez à votre profil
2. Cliquez "Copier Code"
3. Envoyez le code par email
4. Votre collègue entre le code dans le scanner

---

## 📊 Informations Affichées

Quand quelqu'un scanne votre QR code, il verra:

- ✅ **Nom d'utilisateur**: admin
- ✅ **Nom complet**: Administrateur Système
- ✅ **Email**: admin@municipality.tn
- ✅ **Rôle**: Administrateur
- ✅ **Code QR**: USR001
- ✅ **Date de création**: 13/11/2025

---

## 🎯 Cas d'Usage

### Cas 1: Identification Rapide
```
1. Vous arrivez à une réunion
2. Vous partagez votre QR code
3. Les autres scannent votre code
4. Ils voient vos informations
5. Ils peuvent vous contacter
```

### Cas 2: Accès à un Système
```
1. Vous avez besoin d'accéder à un système
2. Vous montrez votre QR code
3. L'administrateur scanne votre code
4. Il voit votre rôle et permissions
5. Il vous donne accès
```

### Cas 3: Partage de Contact
```
1. Vous téléchargez votre QR code
2. Vous l'imprimez sur votre badge
3. Les gens scannent votre badge
4. Ils voient vos informations
5. Ils peuvent vous contacter
```

---

## 🔐 Sécurité

### Données Affichées
- ✅ Informations publiques uniquement
- ✅ Pas de mot de passe
- ✅ Pas de données sensibles
- ✅ Pas de données financières

### Accès Public
- ✅ Pas d'authentification requise
- ✅ Accessible à tous
- ✅ Idéal pour le partage

### Protection
- ✅ Validation du code QR
- ✅ Gestion d'erreurs
- ✅ Messages d'erreur clairs

---

## 📱 Utiliser sur Mobile

### Sur Smartphone/Tablette
1. Allez à `http://localhost:3000/profile`
2. Vous verrez votre QR code
3. Vous pouvez le télécharger
4. Vous pouvez le copier

### Responsive Design
- ✅ Écran complet adapté
- ✅ QR code lisible
- ✅ Boutons tactiles
- ✅ Texte lisible

---

## 🔄 Flux de Données

```
1. Utilisateur va à /profile
2. Frontend récupère les données utilisateur
3. Frontend génère l'image QR
4. Utilisateur voit son QR code
5. Utilisateur télécharge ou copie
6. Utilisateur partage
7. Quelqu'un d'autre scanne le code
8. Frontend envoie GET /api/users/qr/USR001
9. Backend retourne les données utilisateur
10. Frontend affiche les informations
```

---

## 📞 Support

Pour plus d'informations:
- Consultez `QR_SCANNER_GUIDE.md`
- Consultez `HOW_TO_CREATE_QR.md`
- Consultez `MESSAGING_GUIDE.md`

---

## ✅ Checklist

- [ ] Page Profile accessible
- [ ] QR code généré
- [ ] QR code visible
- [ ] Téléchargement fonctionne
- [ ] Copie fonctionne
- [ ] Code QR scannable
- [ ] Informations affichées correctement
- [ ] Accès public confirmé
- [ ] Responsive sur mobile

---

**Bon partage! 👤**

**Dernière mise à jour**: Novembre 2024
