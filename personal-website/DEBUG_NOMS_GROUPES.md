# 🔍 DEBUG: Affichage Noms dans Groupes

## ✅ Modifications Debug Ajoutées

**Fichier:** `frontend/src/pages/Messenger.js` lignes 1289-1300

**Code ajouté:**
```javascript
// Debug: afficher les valeurs
if (msg.id && selectedConversation?.type === 'group') {
  console.log('🔍 Message groupe:', {
    msg_id: msg.id,
    isGroupChat,
    isOwnMessage,
    shouldShowSenderInfo,
    senderName,
    sender_id: msg.sender_id,
    user_id: user.id
  });
}
```

---

## 🧪 Test à Effectuer

### **Étape 1: Vider le Cache**
```
1. Ctrl + Shift + Delete
2. Cocher "Images et fichiers en cache"
3. Effacer
```

### **Étape 2: Ouvrir DevTools**
```
1. F12
2. Onglet Console
3. Vider la console (icône 🚫)
```

### **Étape 3: Tester**
```
1. Ouvrir un groupe (ex: "personeel")
2. Observer la console
```

---

## 📊 Résultats Attendus dans la Console

### **Si le code fonctionne:**
```javascript
🔍 Message groupe: {
  msg_id: 123,
  isGroupChat: true,          // ✅ Doit être true
  isOwnMessage: true,          // Si c'est votre message
  shouldShowSenderInfo: true,  // ✅ Doit être true dans les groupes
  senderName: "Administrateur Système",
  sender_id: 1,
  user_id: 1
}
```

### **Si shouldShowSenderInfo = false:**
Cela signifie que:
- Soit `isGroupChat = false` (le type n'est pas 'group')
- Soit il y a un problème de logique

---

## 🔧 Solutions Possibles

### **Problème 1: Cache Navigateur**
```bash
# Solution:
Ctrl + Shift + Delete → Effacer
Ctrl + Shift + R (plusieurs fois)
```

### **Problème 2: selectedConversation.type n'est pas 'group'**
```javascript
// Vérifier dans la console:
console.log(selectedConversation);
// Doit afficher: { type: 'group', group: {...}, ... }
```

### **Problème 3: Bundle JavaScript pas à jour**
```bash
cd frontend
rm -rf node_modules/.cache
npm start
```

---

## 📝 Checklist Debug

- [ ] Cache navigateur vidé
- [ ] DevTools Console ouverte
- [ ] Logs "🔍 Message groupe:" visibles
- [ ] `isGroupChat: true` dans les logs
- [ ] `shouldShowSenderInfo: true` dans les logs
- [ ] Si tout est true → Problème CSS
- [ ] Si false → Problème logique

---

## 🎯 Actions Selon les Logs

### **Si isGroupChat = false:**
```javascript
// Le selectedConversation n'a pas type: 'group'
// Vérifier comment le groupe est sélectionné
```

### **Si shouldShowSenderInfo = true mais rien ne s'affiche:**
```css
/* Problème CSS - Vérifier les styles */
.message-header {
  display: flex !important;
  visibility: visible !important;
}
```

### **Si pas de logs du tout:**
```javascript
// Le code n'est pas chargé
// → Cache navigateur pas vidé
// → Faire Ctrl+Shift+R plusieurs fois
```

---

## 💡 Test Rapide Alternative

**Dans la Console (F12):**
```javascript
// Vérifier si le nouveau code est présent
const messages = document.querySelectorAll('.message-header');
console.log('Headers trouvés:', messages.length);

// Si = 0, le code n'est pas chargé (cache)
// Si > 0, le code est chargé mais caché (CSS)
```

---

**EFFECTUEZ LE TEST ET PARTAGEZ LES LOGS DE LA CONSOLE!** 🔍
