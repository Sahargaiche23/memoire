# 🧪 GUIDE DE TEST - IMAGES ET APPELS COMME FACEBOOK

**Date:** 13 Novembre 2025  
**Heure:** 17:28

---

## 🎯 TEST 1: IMAGES AVEC MULTER

### Étapes

```bash
1. Allez à http://localhost:3000/messenger
2. Connectez-vous: admin / admin123
3. Sélectionnez une conversation
4. Cliquez "+" (Ajouter image)
5. Sélectionnez une image (JPG, PNG, GIF)
6. ✅ L'image doit s'ajouter au message
7. Cliquez "Envoyer"
8. ✅ L'image doit s'afficher dans le chat
9. Cliquez sur l'image
10. ✅ La modal doit s'ouvrir en plein écran
```

### Résultat Attendu

```
✅ Image uploadée au serveur (/backend/uploads)
✅ URL persistante: http://localhost:5000/api/uploads/1234567890_image.jpg
✅ Affichée dans le chat
✅ Ouvrable en plein écran
```

---

## 🎯 TEST 2: APPELS ENREGISTRÉS DANS LES MESSAGES

### Étapes

```bash
1. Allez à Messenger
2. Sélectionnez une conversation
3. Cliquez "📞" (Appel audio)
4. Attendez 2 secondes
5. Cliquez "✅ Accepter"
6. La modal d'appel s'ouvre
7. Attendez 10 secondes
8. Cliquez "Terminer l'appel"
9. ✅ L'appel doit s'enregistrer dans les messages
10. ✅ Vous devriez voir: "📞 Appel vocal - 10s"
```

### Résultat Attendu

```
✅ Appel enregistré comme message
✅ Affichage: "📞 Appel vocal - 10s"
✅ Visible dans l'historique
✅ Comme Facebook!
```

---

## 🎯 TEST 3: AFFICHAGE COMME FACEBOOK

### Images - Affichage Attendu

```
[Avatar] Nom Utilisateur
[Image]
Date et Heure
```

### Appels - Affichage Attendu

```
[Avatar Rouge] Appel vocal manqué
22:50
[Bouton] Rappeler
```

---

## 📊 CHECKLIST

- [ ] Images uploadées au serveur
- [ ] Images affichées dans le chat
- [ ] Images ouvrables en plein écran
- [ ] Appels enregistrés dans les messages
- [ ] Appels affichent la durée
- [ ] Affichage comme Facebook
- [ ] Avatar + Nom utilisateur
- [ ] Bouton "Rappeler" visible
- [ ] Tous les tests passent

---

## 🔧 DÉPANNAGE

### Images ne s'affichent pas

```bash
1. Vérifier le dossier: /backend/uploads
2. Vérifier la console: F12 > Console
3. Vérifier l'URL: http://localhost:5000/api/uploads/
4. Vérifier le backend: http://localhost:5000 (pas d'erreur)
```

### Appels ne s'enregistrent pas

```bash
1. Vérifier la console: F12 > Console
2. Vérifier le backend: http://localhost:5000/api/calls/log
3. Vérifier la base de données: messages table
4. Vérifier les logs: Terminal backend
```

---

**GUIDE DE TEST COMPLET! 🚀**
