# 🧪 Guide de Test - Nouvelles Fonctionnalités v1.2.0

## 🎯 Tester les 3 Nouvelles Fonctionnalités

Ce guide vous montre comment tester Chatbot, Messagerie et QR Scanner.

---

## 📧 1. Tester la Messagerie

### Étape 1: Accéder à la Page Messages
1. Connectez-vous avec `admin / admin123`
2. Cliquez sur **"📧 Messages"** dans la navigation
3. Vous devriez voir la page de messagerie

### Étape 2: Envoyer un Message
1. Cliquez sur **"+ Nouveau Message"**
2. Remplissez le formulaire:
   - **Destinataire:** Sélectionnez un utilisateur (ex: responsable)
   - **Sujet:** "Test de messagerie"
   - **Message:** "Ceci est un test"
3. Cliquez sur **"Envoyer"**
4. Vous devriez voir: "Message envoyé avec succès!"

### Étape 3: Vérifier les Messages Reçus
1. Connectez-vous avec un autre compte (ex: `responsable / pass123`)
2. Allez à **"📧 Messages"**
3. Vous devriez voir le message reçu
4. Cliquez sur **"Marquer comme lu"**

### ✅ Checklist Messagerie
- [ ] Page Messages accessible
- [ ] Formulaire d'envoi fonctionne
- [ ] Message envoyé avec succès
- [ ] Message reçu par le destinataire
- [ ] Marquer comme lu fonctionne

---

## 🤖 2. Tester le Chatbot

### Étape 1: Accéder à la Page Chatbot
1. Connectez-vous avec `admin / admin123`
2. Cliquez sur **"🤖 Chatbot"** dans la navigation
3. Vous devriez voir l'interface de chat

### Étape 2: Poser une Question
1. Cliquez dans le champ d'entrée
2. Tapez: **"Comment créer un actif?"**
3. Cliquez sur **"Envoyer"** ou appuyez sur Entrée
4. Vous devriez voir la réponse du chatbot

### Étape 3: Utiliser les Questions Rapides
1. Cliquez sur une question rapide (ex: "Aide")
2. La question s'ajoute au champ d'entrée
3. Cliquez sur Envoyer
4. Vous devriez voir la réponse

### Étape 4: Consulter l'Historique
1. Regardez la barre latérale droite
2. Vous devriez voir l'historique des conversations
3. Cliquez sur une question pour la relancer

### Étape 5: Réinitialiser
1. Cliquez sur **"Réinitialiser"** en haut
2. La conversation devrait être réinitialisée

### ✅ Checklist Chatbot
- [ ] Page Chatbot accessible
- [ ] Envoi de message fonctionne
- [ ] Réponse du chatbot affichée
- [ ] Questions rapides fonctionnent
- [ ] Historique visible
- [ ] Réinitialisation fonctionne

---

## 📱 3. Tester le QR Scanner

### Étape 1: Accéder à la Page QR Scanner
1. **Sans se connecter**, allez à: `http://localhost:3000/qr-scanner`
2. Vous devriez voir la page de scanner QR

### Étape 2: Entrer un Code QR
1. Dans le champ d'entrée, tapez: **QR001**
2. Cliquez sur **"Rechercher"**
3. Vous devriez voir les détails de l'actif

### Étape 3: Vérifier les Informations
1. Vous devriez voir:
   - Nom de l'actif
   - Catégorie
   - Localisation
   - Valeur d'acquisition
   - Valeur actuelle
   - Description

### Étape 4: Imprimer
1. Cliquez sur **"🖨️ Imprimer"**
2. La page d'impression devrait s'ouvrir

### Étape 5: Nouveau Scan
1. Cliquez sur **"🔄 Nouveau Scan"**
2. Le formulaire devrait être réinitialisé

### Étape 6: Tester avec d'Autres QR Codes
Essayez d'autres codes QR (générés automatiquement pour chaque actif):
- QR001 - Mairie Centrale
- QR002 - Centre de Santé
- QR003 - Bibliothèque Municipale
- etc.

### ✅ Checklist QR Scanner
- [ ] Page QR Scanner accessible sans authentification
- [ ] Entrée de code QR fonctionne
- [ ] Recherche fonctionne
- [ ] Détails de l'actif affichés
- [ ] Impression fonctionne
- [ ] Nouveau Scan réinitialise
- [ ] Accès public confirmé

---

## 🧪 Tests Avancés

### Test 1: Messagerie Multi-Utilisateurs
```
1. Connectez-vous en tant qu'admin
2. Envoyez un message à responsable
3. Déconnectez-vous
4. Connectez-vous en tant que responsable
5. Vérifiez que vous avez reçu le message
6. Répondez au message
7. Reconnectez-vous en tant qu'admin
8. Vérifiez la réponse
```

### Test 2: Chatbot par Rôle
```
1. Connectez-vous en tant qu'admin
2. Posez une question au chatbot
3. Notez la réponse
4. Déconnectez-vous
5. Connectez-vous en tant que responsable_patrimoine
6. Posez la même question
7. Comparez les réponses (elles doivent être adaptées au rôle)
```

### Test 3: QR Scanner Mobile
```
1. Ouvrez http://localhost:3000/qr-scanner sur un mobile/tablette
2. Testez la responsivité
3. Entrez un code QR
4. Vérifiez que l'affichage est correct
5. Testez l'impression
```

---

## 🐛 Dépannage

### Messagerie ne fonctionne pas
```
1. Vérifiez que le backend démarre sans erreur
2. Vérifiez que vous êtes connecté
3. Vérifiez que les utilisateurs existent
4. Consultez la console du navigateur (F12)
```

### Chatbot ne répond pas
```
1. Vérifiez que le backend démarre sans erreur
2. Vérifiez que vous êtes connecté
3. Vérifiez que vous avez un rôle valide
4. Consultez la console du navigateur (F12)
```

### QR Scanner ne trouve pas l'actif
```
1. Vérifiez que la base de données est initialisée
2. Vérifiez que vous avez entré le bon code QR
3. Vérifiez que l'actif existe dans la BD
4. Consultez la console du navigateur (F12)
```

---

## 📊 Résultats Attendus

### Messagerie
- ✅ Page charge correctement
- ✅ Formulaire d'envoi fonctionne
- ✅ Messages affichés correctement
- ✅ Statut "Non lu" visible
- ✅ Marquer comme lu fonctionne

### Chatbot
- ✅ Page charge correctement
- ✅ Messages affichés correctement
- ✅ Réponses adaptées au rôle
- ✅ Historique visible
- ✅ Questions rapides fonctionnent
- ✅ Indicateur de frappe animé

### QR Scanner
- ✅ Page charge sans authentification
- ✅ Recherche fonctionne
- ✅ Détails affichés correctement
- ✅ Impression fonctionne
- ✅ Responsive sur mobile
- ✅ Accès public confirmé

---

## 🎯 Cas d'Usage Réels

### Scénario 1: Agent sur le Terrain
```
1. Agent arrive sur site
2. Va à http://localhost:3000/qr-scanner
3. Scanne le QR Code de l'actif
4. Voit les informations
5. Effectue l'intervention
6. Enregistre le résultat
```

### Scénario 2: Communication Admin-Agent
```
1. Admin envoie un message à l'agent
2. Agent reçoit la notification
3. Agent consulte le message
4. Agent répond
5. Admin reçoit la réponse
```

### Scénario 3: Aide Contextuelle
```
1. Utilisateur ouvre le chatbot
2. Pose une question
3. Reçoit une réponse adaptée à son rôle
4. Consulte l'historique
5. Relance une question précédente
```

---

## ✅ Validation Complète

Après avoir testé les 3 fonctionnalités, vous devriez avoir:

- ✅ Messagerie fonctionnelle
- ✅ Chatbot fonctionnel
- ✅ QR Scanner fonctionnel
- ✅ Toutes les pages accessibles
- ✅ Tous les formulaires fonctionnent
- ✅ Tous les boutons fonctionnent
- ✅ Responsive design confirmé
- ✅ Accès public pour QR Scanner confirmé

---

## 📞 Support

Si vous rencontrez des problèmes:
1. Consultez la console du navigateur (F12)
2. Vérifiez les logs du backend
3. Vérifiez que la base de données est initialisée
4. Consultez `NEW_FEATURES.md` pour plus de détails

---

**Bon test! 🎉**

**Dernière mise à jour**: Novembre 2024
