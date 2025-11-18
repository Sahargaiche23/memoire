# 🧪 Guide de Test - Page Profile

## Préparation
1. **Backend lancé** : `python3 app.py` (port 5000)
2. **Frontend lancé** : `npm start` (port 3000)
3. **Connecté comme utilisateur** avec un QR code

## Tests des Fonctionnalités

### ✅ Test 1: Photo de Profil
1. Cliquez sur l'avatar rond en haut
2. Sélectionnez une image (< 5MB)
3. **Résultat attendu** :
   - Console: "📸 Fonction handleProfileImageChange appelée"
   - Console: "📤 Uploading vers backend..."
   - Alert: "✅ Photo de profil uploadée avec succès!"
   - L'image s'affiche immédiatement

### ✅ Test 2: Télécharger QR Code
1. Cliquez sur le bouton "Télécharger QR"
2. **Résultat attendu** :
   - Console: "🔽 Fonction downloadQR appelée"
   - Console: "📥 Début du téléchargement..."
   - Console: "✅ Téléchargement réussi!"
   - Alert: "✅ QR Code téléchargé avec succès!"
   - Fichier téléchargé: `username_qr_code.png`

### ✅ Test 3: Copier Code QR
1. Cliquez sur le bouton "Copier Code"
2. **Résultat attendu** :
   - Console: "📋 Fonction copyQRCode appelée"
   - Console: "✅ Copie réussie!"
   - Bouton devient VERT pendant 2 secondes
   - Alert: "✅ Code QR copié dans le presse-papier!"
   - Le code est dans le presse-papier (Ctrl+V pour vérifier)

### ✅ Test 4: Tester Scanner
1. Cliquez sur le bouton "Tester Scanner"
2. **Résultat attendu** :
   - Console: "🧪 Fonction testScanner appelée"
   - Console: "✅ Fenêtre ouverte avec succès"
   - Alert: "✅ Scanner ouvert dans un nouvel onglet!"
   - Nouvel onglet s'ouvre vers `/qr-scanner?code=XXX`
   - Le code est pré-rempli dans le scanner

### ✅ Test 5: Modifier le Profil
1. Cliquez sur "Modifier le Profil" (bouton violet en haut)
2. Modifiez le nom et/ou l'email
3. Cliquez sur "Enregistrer"
4. **Résultat attendu** :
   - Console: "💾 Fonction handleSaveProfile appelée"
   - Console: "✅ Mise à jour réussie:"
   - Alert: "✅ Profil mis à jour avec succès!"
   - La page se recharge
   - Les nouvelles données sont affichées

### ✅ Test 6: Scanner Caméra
1. Cliquez sur "Scanner Caméra"
2. Autorisez l'accès à la caméra
3. **Résultat attendu** :
   - Console: "📷 Fonction startCameraScanner appelée"
   - Console: "🎥 Demande d'accès à la caméra..."
   - Console: "✅ Accès caméra accordé"
   - Modal s'ouvre avec flux vidéo
   - Cadre de scan animé visible

## Vérification Backend

### Logs Backend Attendus:
```
127.0.0.1 - - [14/Nov/2025 XX:XX:XX] "POST /api/upload HTTP/1.1" 200 -
127.0.0.1 - - [14/Nov/2025 XX:XX:XX] "PUT /api/users/X HTTP/1.1" 200 -
```

## Problèmes Courants

### ❌ "QR Code non trouvé"
- Vérifiez que l'utilisateur a un QR code dans la base de données
- Vérifiez `/qr_codes/` contient les images

### ❌ "Erreur 401 Unauthorized"
- Le token JWT a expiré, reconnectez-vous

### ❌ "Popup bloqué"
- Autorisez les pop-ups pour localhost:3000

### ❌ "Erreur upload"
- Vérifiez que le dossier `/uploads/` existe
- Vérifiez les permissions du dossier

## Console de Débogage

Ouvrez la **console du navigateur** (F12) pour voir TOUS les logs :
- 🔽 downloadQR
- 📋 copyQRCode  
- 🧪 testScanner
- 📸 handleProfileImageChange
- 💾 handleSaveProfile
- 📷 startCameraScanner

Chaque fonction affiche son nom au début pour confirmer qu'elle est appelée!

## Test Complet Réussi ✅

Si tous les tests passent, vous devriez voir:
1. ✅ Photo de profil modifiée
2. ✅ QR Code téléchargé  
3. ✅ Code copié
4. ✅ Scanner ouvert
5. ✅ Profil modifié et enregistré
6. ✅ Caméra activée

**Tous les boutons sont dynamiques et fonctionnels!**
