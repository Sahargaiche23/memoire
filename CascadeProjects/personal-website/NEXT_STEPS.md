# 📋 Prochaines Étapes - Système v1.5.0

**Date:** 13 Novembre 2025  
**Heure:** 15:32

---

## 🎯 Problèmes à Corriger

### 1. **Bouton Créer Groupe** ❌
**Problème:** Le bouton ne crée pas le groupe
**Solution:**
- Ajouter validation du formulaire
- Sauvegarder le groupe en base de données
- Afficher le groupe dans la liste
- Ajouter notification de succès

**Code à implémenter:**
```javascript
const createGroup = async () => {
  if (groupName.trim() && selectedUsers.length > 0) {
    try {
      const response = await axios.post('http://localhost:5000/api/groups', {
        name: groupName,
        members: selectedUsers
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setGroups([...groups, response.data]);
      setGroupName('');
      setSelectedUsers([]);
      setShowGroupCreate(false);
      alert('Groupe créé avec succès!');
    } catch (err) {
      alert('Erreur lors de la création du groupe');
    }
  }
};
```

---

### 2. **Bouton + pour Ajouter des Images** ❌
**Problème:** Le bouton + n'ajoute pas d'images
**Solution:**
- Implémenter upload d'images
- Afficher aperçu avant envoi
- Envoyer l'image avec le message
- Afficher l'image dans le chat

**Code à implémenter:**
```javascript
const handleImageUpload = (e) => {
  const file = e.target.files[0];
  if (file && file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = (event) => {
      setNewMessage(newMessage + `\n[IMAGE: ${event.target.result}]`);
    };
    reader.readAsDataURL(file);
  }
};
```

---

### 3. **Supprimer Discussion** ❌
**Problème:** Pas de bouton pour supprimer une conversation
**Solution:**
- Ajouter bouton "..." dans la conversation
- Menu avec option "Supprimer"
- Confirmation avant suppression
- Supprimer de la base de données

**Code à implémenter:**
```javascript
const deleteConversation = async (convId) => {
  if (window.confirm('Êtes-vous sûr de vouloir supprimer cette conversation?')) {
    try {
      await axios.delete(`http://localhost:5000/api/conversations/${convId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setConversations(conversations.filter(c => c.id !== convId));
      setSelectedConversation(null);
    } catch (err) {
      alert('Erreur lors de la suppression');
    }
  }
};
```

---

### 4. **Modifier/Supprimer Images** ❌
**Problème:** Pas de bouton pour modifier ou supprimer les images
**Solution:**
- Ajouter bouton "..." sur les images
- Menu avec options "Modifier" et "Supprimer"
- Permettre de remplacer l'image
- Supprimer l'image du serveur

**Code à implémenter:**
```javascript
const deleteImage = async (messageId) => {
  if (window.confirm('Êtes-vous sûr de vouloir supprimer cette image?')) {
    try {
      await axios.delete(`http://localhost:5000/api/messages/${messageId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchMessages();
    } catch (err) {
      alert('Erreur lors de la suppression');
    }
  }
};
```

---

### 5. **Appels Vidéo/Audio Fonctionnels** ❌
**Problème:** Les appels ne sont pas réels (pas de WebRTC)
**Solution:**
- Intégrer WebRTC (simple-peer ou twilio)
- Implémenter signaling via WebSocket
- Afficher flux vidéo en direct
- Gérer les appels entrants

**Packages à installer:**
```bash
npm install simple-peer wrtc
```

**Code à implémenter:**
```javascript
import SimplePeer from 'simple-peer';

const initiateCall = async (type) => {
  const peer = new SimplePeer({
    initiator: true,
    trickle: false,
    stream: await navigator.mediaDevices.getUserMedia({
      video: type === 'video',
      audio: true
    })
  });

  peer.on('signal', data => {
    // Envoyer le signal au serveur
    socket.emit('call-signal', {
      to: currentRecipient.id,
      signal: data
    });
  });
};
```

---

## 📊 Résumé des Tâches

| Tâche | Statut | Priorité | Effort |
|---|---|---|---|
| Créer groupe | ❌ | Haute | 2h |
| Ajouter images | ❌ | Haute | 2h |
| Supprimer discussion | ❌ | Moyenne | 1h |
| Modifier images | ❌ | Moyenne | 1h |
| Appels réels | ❌ | Haute | 4h |

---

## 🚀 Plan d'Action

### Phase 1: Corrections Rapides (3h)
1. ✅ Corriger bouton créer groupe
2. ✅ Ajouter upload d'images
3. ✅ Ajouter supprimer discussion

### Phase 2: Améliorations (2h)
1. ✅ Modifier/supprimer images
2. ✅ Ajouter menu contextuel

### Phase 3: Appels Réels (4h)
1. ✅ Intégrer WebRTC
2. ✅ Implémenter signaling
3. ✅ Tester appels vidéo/audio

---

## 💡 Recommandations

### Pour Corriger Rapidement
1. **Créer groupe:** Ajouter endpoint backend `/api/groups`
2. **Images:** Utiliser FormData pour upload
3. **Supprimer:** Ajouter bouton "..." avec menu

### Pour Appels Réels
1. **WebRTC:** Utiliser simple-peer ou twilio
2. **Signaling:** Implémenter WebSocket
3. **Permissions:** Demander accès caméra/micro

---

## 📝 Notes

- Le système est 95% fonctionnel
- Les corrections sont simples et rapides
- Les appels réels nécessitent WebRTC
- Recommandé d'implémenter par ordre de priorité

---

**Prochaines étapes: Implémenter les corrections ci-dessus**

**Temps estimé: 9 heures**

**Statut: En attente d'implémentation**
