# 📧 Guide Complet - Messagerie avec Réponses

## 🎯 Vue d'ensemble

La messagerie permet la communication entre utilisateurs avec système de réponses directes.

---

## 🚀 Accéder à la Messagerie

### Depuis la Navbar
1. Connectez-vous avec vos identifiants
2. Cliquez sur **"📧 Messages"** dans la navigation
3. Vous verrez la page de messagerie

---

## 📨 Envoyer un Message

### Étape 1: Cliquer sur "Nouveau Message"
1. Allez à la page **Messages**
2. Cliquez sur le bouton bleu **"+ Nouveau Message"**

### Étape 2: Remplir le Formulaire
Le formulaire contient:
- **Destinataire** (liste déroulante)
- **Sujet** (texte court)
- **Message** (texte long)

### Étape 3: Sélectionner le Destinataire
1. Cliquez sur le champ "Destinataire"
2. Sélectionnez un utilisateur dans la liste
3. Exemples:
   - Mohamed Ben Ali (Responsable Patrimoine)
   - Ahmed Khaled (Agent Maintenance)
   - Fatima Zahra (Auditeur)
   - Omar Saïd (Responsable Service)

### Étape 4: Écrire le Sujet
Exemples:
- "Demande de maintenance"
- "Rapport d'inspection"
- "Question sur l'actif"
- "Coordination de projet"

### Étape 5: Écrire le Message
Écrivez votre message complet dans le champ texte.

### Étape 6: Envoyer
Cliquez sur **"Envoyer"**

Vous devriez voir: **"✅ Message envoyé avec succès!"**

---

## 📬 Recevoir et Lire les Messages

### Voir les Messages Reçus
1. Allez à la page **Messages**
2. Vous verrez la section **"Messages Reçus (X)"**
3. Chaque message affiche:
   - Nom de l'expéditeur
   - Date de réception
   - Sujet du message
   - Statut (lu/non lu)

### Lire un Message
1. Cliquez sur le message que vous voulez lire
2. Le message s'ouvre et affiche:
   - Expéditeur
   - Date
   - Sujet
   - Contenu complet
   - Bouton "Répondre"

### Marquer comme Lu
1. Cliquez sur le bouton **"✓ Marquer comme lu"**
2. Le statut change de "Non lu" à "Lu"

---

## 💬 Répondre à un Message

### Système de Réponses

**Important:** Le système actuel utilise un système de **réponses par message distinct**.

Pour répondre:
1. Lisez le message reçu
2. Cliquez sur **"Répondre"**
3. Un nouveau formulaire s'ouvre
4. Le destinataire est automatiquement l'expéditeur original
5. Le sujet est pré-rempli avec "RE: [sujet original]"
6. Écrivez votre réponse
7. Cliquez sur **"Envoyer"**

### Exemple de Conversation

**Message 1 (Admin → Responsable):**
```
Sujet: Demande de maintenance
Message: Pouvez-vous vérifier le serveur?
```

**Message 2 (Responsable → Admin):**
```
Sujet: RE: Demande de maintenance
Message: Oui, je vais vérifier demain matin.
```

**Message 3 (Admin → Responsable):**
```
Sujet: RE: Demande de maintenance
Message: Merci, c'est urgent!
```

---

## 🧪 Scénario Complet de Test

### Étape 1: Envoyer un Message (Admin)
1. Connectez-vous avec **admin / admin123**
2. Allez à **Messages**
3. Cliquez sur **"+ Nouveau Message"**
4. Remplissez:
   - Destinataire: **Mohamed Ben Ali**
   - Sujet: **"Test de messagerie"**
   - Message: **"Ceci est un test de messagerie. Pouvez-vous répondre?"**
5. Cliquez sur **"Envoyer"**
6. Vous devriez voir: **"✅ Message envoyé avec succès!"**

### Étape 2: Recevoir le Message (Responsable)
1. Déconnectez-vous (cliquez sur le bouton Déconnexion)
2. Connectez-vous avec **responsable / pass123**
3. Allez à **Messages**
4. Vous devriez voir le message reçu:
   - Expéditeur: "Administrateur Système"
   - Sujet: "Test de messagerie"
   - Statut: "Non lu" (badge rouge)

### Étape 3: Lire et Répondre (Responsable)
1. Cliquez sur le message pour le lire
2. Lisez le contenu complet
3. Cliquez sur **"Répondre"**
4. Un formulaire s'ouvre avec:
   - Destinataire: **Administrateur Système** (pré-rempli)
   - Sujet: **RE: Test de messagerie** (pré-rempli)
5. Écrivez votre réponse:
   - Message: **"Oui, j'ai bien reçu votre message. Tout fonctionne!"**
6. Cliquez sur **"Envoyer"**
7. Vous devriez voir: **"✅ Message envoyé avec succès!"**

### Étape 4: Vérifier la Réponse (Admin)
1. Déconnectez-vous
2. Reconnectez-vous avec **admin / admin123**
3. Allez à **Messages**
4. Vous devriez voir la réponse:
   - Expéditeur: "Mohamed Ben Ali"
   - Sujet: "RE: Test de messagerie"
   - Statut: "Non lu"

### Étape 5: Continuer la Conversation
1. Cliquez sur la réponse pour la lire
2. Cliquez sur **"Répondre"**
3. Écrivez une nouvelle réponse
4. Cliquez sur **"Envoyer"**

---

## 👥 Utilisateurs Disponibles

Vous pouvez envoyer des messages à:

| Utilisateur | Nom Complet | Rôle |
|-------------|-------------|------|
| admin | Administrateur Système | Admin |
| responsable | Mohamed Ben Ali | Responsable Patrimoine |
| agent | Ahmed Khaled | Agent Maintenance |
| auditeur | Fatima Zahra | Auditeur |
| service_chief | Omar Saïd | Responsable Service |

---

## 📊 Informations Affichées

### Pour Chaque Message Reçu
- ✅ Nom de l'expéditeur
- ✅ Rôle de l'expéditeur
- ✅ Date de réception
- ✅ Sujet
- ✅ Statut (lu/non lu)
- ✅ Bouton "Marquer comme lu"

### Dans le Détail du Message
- ✅ Expéditeur complet
- ✅ Date et heure
- ✅ Sujet
- ✅ Contenu complet
- ✅ Bouton "Répondre"

---

## 🎯 Cas d'Usage Réels

### Cas 1: Demande de Maintenance
```
1. Admin envoie: "Pouvez-vous vérifier le serveur?"
2. Responsable reçoit et lit
3. Responsable répond: "Je vais vérifier demain"
4. Admin reçoit la réponse
5. Admin répond: "Merci, c'est urgent"
```

### Cas 2: Rapport d'Inspection
```
1. Agent envoie: "Inspection terminée, tout OK"
2. Responsable reçoit et lit
3. Responsable répond: "Merci pour le rapport"
4. Agent reçoit la confirmation
```

### Cas 3: Coordination de Projet
```
1. Responsable envoie: "Réunion demain à 10h"
2. Plusieurs utilisateurs reçoivent
3. Chacun répond: "OK, je serai présent"
4. Responsable reçoit toutes les confirmations
```

---

## ✅ Checklist de Test

- [ ] Page Messages accessible
- [ ] Formulaire "Nouveau Message" fonctionne
- [ ] Destinataires affichés correctement
- [ ] Message envoyé avec succès
- [ ] Message reçu par le destinataire
- [ ] Message visible dans la liste
- [ ] Message peut être lu
- [ ] Statut "Non lu" visible
- [ ] Bouton "Marquer comme lu" fonctionne
- [ ] Bouton "Répondre" fonctionne
- [ ] Réponse envoyée avec succès
- [ ] Réponse reçue par l'expéditeur original
- [ ] Conversation complète visible

---

## 🔄 Flux de Données

```
1. Utilisateur A envoie un message
2. Frontend envoie POST /api/messages
3. Backend crée le message en BD
4. Utilisateur B reçoit une notification
5. Utilisateur B consulte Messages
6. Frontend récupère GET /api/messages
7. Backend retourne les messages reçus
8. Utilisateur B lit le message
9. Utilisateur B clique "Répondre"
10. Nouveau message créé avec sujet "RE: ..."
11. Utilisateur A reçoit la réponse
12. Conversation continue...
```

---

## 📞 Support

Pour plus d'informations:
- Consultez `TEST_NEW_FEATURES.md`
- Consultez `NEW_FEATURES.md`
- Consultez `GUIDE_UTILISATION.md`

---

**Bon messaging! 📧**

**Dernière mise à jour**: Novembre 2024
