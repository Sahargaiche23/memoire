# 🧪 TEST COMPLET FINAL - SYSTÈME v1.7.0

**Date:** 13 Novembre 2025  
**Heure:** 17:33

---

## 🚀 ÉTAPE 1: REDÉMARRER LES SERVEURS

### Terminal 1 - Backend
```bash
cd /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend
pkill -f "python3 app.py"
sleep 2
python3 app.py
```

✅ Vous devriez voir: `Running on http://localhost:5000`

### Terminal 2 - Frontend
```bash
cd /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/frontend
pkill -f "npm start"
sleep 2
npm start
```

✅ Vous devriez voir: `Compiled successfully`

---

## 🧪 ÉTAPE 2: TEST IMAGES AVEC MULTER

### Étapes Précises

```
1. Allez à http://localhost:3000
2. Connectez-vous: admin / admin123
3. Cliquez "Messenger"
4. Sélectionnez "sahargaziche"
5. Cliquez "+" (Ajouter image)
6. Sélectionnez une image JPG/PNG
7. ✅ L'image doit s'ajouter au message
8. Cliquez "Envoyer"
9. ✅ L'image doit s'afficher avec:
   - Avatar (S)
   - Nom: "sahargaziche"
   - L'image
   - Heure
10. Cliquez sur l'image
11. ✅ La modal doit s'ouvrir en plein écran
```

### Résultat Attendu

```
✅ Image uploadée à: /backend/uploads/1234567890_image.jpg
✅ URL: http://localhost:5000/api/uploads/1234567890_image.jpg
✅ Affichée dans le chat
✅ Ouvrable en plein écran
✅ Avatar + Nom visible
```

---

## 🧪 ÉTAPE 3: TEST APPELS ENREGISTRÉS

### Étapes Précises

```
1. Sélectionnez une conversation
2. Cliquez "📞" (Appel audio)
3. ✅ Notification s'affiche (haut à droite)
4. Cliquez "✅ Accepter"
5. ✅ La modal d'appel s'ouvre
6. Attendez 15 secondes
7. Cliquez "Terminer l'appel"
8. ✅ L'appel doit s'enregistrer dans les messages
9. ✅ Vous devriez voir:
   - Avatar rouge (📞)
   - "📞 Appel vocal - 15s"
   - Bouton "Rappeler"
   - Heure
```

### Résultat Attendu

```
✅ Appel enregistré comme message
✅ Affichage: "📞 Appel vocal - 15s"
✅ Avatar rouge
✅ Bouton "Rappeler" visible
✅ Visible dans l'historique
```

---

## 🧪 ÉTAPE 4: TEST REFUSER UN APPEL

### Étapes Précises

```
1. Sélectionnez une conversation
2. Cliquez "📞" (Appel audio)
3. ✅ Notification s'affiche
4. Cliquez "❌ Refuser"
5. ✅ La notification doit disparaître
6. ✅ L'appel doit s'enregistrer comme "Appel manqué"
7. ✅ Vous devriez voir:
   - Avatar rouge (📞)
   - "📞 Appel vocal manqué - 0s"
   - Bouton "Rappeler"
```

### Résultat Attendu

```
✅ Notification disparaît
✅ Appel enregistré comme manqué
✅ Affichage: "📞 Appel vocal manqué - 0s"
✅ Bouton "Rappeler" visible
```

---

## 📊 CHECKLIST FINALE

- [ ] Backend redémarré (http://localhost:5000)
- [ ] Frontend redémarré (http://localhost:3000)
- [ ] Connexion réussie
- [ ] Image uploadée au serveur
- [ ] Image affichée avec avatar + nom
- [ ] Image ouvrable en plein écran
- [ ] Appel enregistré dans les messages
- [ ] Appel affiche la durée
- [ ] Avatar rouge pour appels
- [ ] Bouton "Rappeler" visible
- [ ] Refuser appel fonctionne
- [ ] Notification disparaît après refus
- [ ] Appel manqué enregistré
- [ ] Tous les tests passent ✅

---

## 🔧 DÉPANNAGE

### Images ne s'affichent pas

```bash
# Vérifier le dossier uploads
ls -la /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/uploads

# Vérifier l'URL dans le navigateur
http://localhost:5000/api/uploads/1234567890_image.jpg

# Vérifier la console
F12 > Console > Chercher les erreurs
```

### Appels ne s'enregistrent pas

```bash
# Vérifier les logs backend
# Chercher: "POST /api/calls/log"

# Vérifier la base de données
# Chercher les messages avec "📞 Appel"

# Vérifier la console frontend
F12 > Console > Chercher les erreurs
```

### Notification reste affichée

```bash
# Cliquer sur "❌ Refuser" doit fermer la notification
# Si ça ne fonctionne pas, rechargez la page (Ctrl+F5)
```

---

## ✅ SUCCÈS

Si tous les tests passent, le système est **100% FONCTIONNEL**!

---

**GUIDE DE TEST COMPLET FINAL! 🚀**
