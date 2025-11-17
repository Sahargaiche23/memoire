# ✨ Nouvelles Fonctionnalités Ajoutées

## 🎯 Vue d'ensemble

Le système a été enrichi avec 3 nouvelles fonctionnalités majeures:
1. **Messagerie entre Utilisateurs**
2. **Chatbot Intelligent**
3. **Support Utilisateur Mobile avec QR Code**

---

## 📧 1. Messagerie Entre Utilisateurs

### Description
Les utilisateurs peuvent communiquer directement via le système de messagerie interne.

### Endpoints API

#### Récupérer les Messages Reçus
```
GET /api/messages
Authorization: Bearer <token>
```

**Réponse:**
```json
[
  {
    "id": 1,
    "sender_id": 2,
    "sender_name": "Mohamed Ben Ali",
    "subject": "Demande de maintenance",
    "content": "Pouvez-vous planifier une maintenance pour le serveur?",
    "is_read": false,
    "created_at": "2025-11-13T13:00:00"
  }
]
```

#### Envoyer un Message
```
POST /api/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "recipient_id": 2,
  "subject": "Demande de maintenance",
  "content": "Pouvez-vous planifier une maintenance pour le serveur?"
}
```

**Réponse:**
```json
{
  "id": 1,
  "message": "Message envoyé"
}
```

#### Marquer un Message comme Lu
```
PUT /api/messages/<message_id>/read
Authorization: Bearer <token>
```

### Cas d'Usage

#### Admin → Agent
```
Admin: "Bonjour, pouvez-vous vérifier le serveur?"
Agent: "Oui, je vais le faire aujourd'hui"
```

#### Responsable Patrimoine → Responsable Service
```
Resp. Patrimoine: "Demande de transfert du véhicule 001"
Resp. Service: "Accepté, nous le récupérons demain"
```

---

## 🤖 2. Chatbot Intelligent

### Description
Un assistant virtuel qui aide les utilisateurs selon leur rôle.

### Endpoints API

#### Envoyer un Message au Chatbot
```
POST /api/chatbot
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "Comment créer un actif?"
}
```

**Réponse:**
```json
{
  "user_message": "Comment créer un actif?",
  "bot_response": "Pour créer un actif, allez à la page Actifs et cliquez sur \"+ Ajouter un actif\".",
  "timestamp": "2025-11-13T13:00:00"
}
```

#### Récupérer l'Historique du Chatbot
```
GET /api/chatbot/history
Authorization: Bearer <token>
```

**Réponse:**
```json
[
  {
    "id": 1,
    "message": "Comment créer un actif?",
    "response": "Pour créer un actif, allez à la page Actifs et cliquez sur \"+ Ajouter un actif\".",
    "created_at": "2025-11-13T13:00:00"
  }
]
```

### Réponses du Chatbot par Rôle

#### Admin
- **utilisateur** → Gestion des utilisateurs
- **rôle** → Rôles disponibles
- **permission** → Permissions par rôle
- **aide** → Aide générale

#### Responsable Patrimoine
- **actif** → Créer un actif
- **maintenance** → Planifier une maintenance
- **rapport** → Générer un rapport
- **aide** → Aide générale

#### Agent Maintenance
- **intervention** → Enregistrer une intervention
- **maintenance** → Consulter les maintenances
- **aide** → Aide générale

#### Auditeur
- **rapport** → Consulter les rapports
- **statistique** → Voir les statistiques
- **aide** → Aide générale

### Exemples de Conversations

```
Utilisateur: "Bonjour"
Chatbot: "Bonjour! Comment puis-je vous aider?"

Utilisateur: "Comment créer un actif?"
Chatbot: "Pour créer un actif, allez à la page Actifs et cliquez sur \"+ Ajouter un actif\"."

Utilisateur: "Merci"
Chatbot: "De rien! N'hésitez pas à me poser d'autres questions."
```

---

## 📱 3. Support Utilisateur Mobile avec QR Code

### Description
Les utilisateurs mobiles peuvent scanner un QR Code pour accéder aux informations d'un actif sans authentification.

### Endpoint API

#### Récupérer un Actif par QR Code
```
GET /api/assets/qr/<qr_code>
```

**Réponse:**
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

### Cas d'Usage

#### Scénario 1: Technicien sur le Terrain
```
1. Technicien arrive sur site
2. Scanne le QR Code de l'actif
3. Accède aux informations (localisation, statut, historique)
4. Effectue l'intervention
5. Enregistre le résultat dans le système
```

#### Scénario 2: Inspection Rapide
```
1. Inspecteur scanne le QR Code
2. Vérifie l'état de l'actif
3. Prend des photos
4. Enregistre les observations
```

### Implémentation Frontend

```javascript
// Scanner QR Code
import QrScanner from 'qr-scanner';

function scanQRCode() {
  const video = document.getElementById('qr-video');
  const qrScanner = new QrScanner(
    video,
    result => {
      // Récupérer l'actif
      fetch(`http://localhost:5000/api/assets/qr/${result.data}`)
        .then(res => res.json())
        .then(asset => {
          // Afficher les informations
          displayAssetInfo(asset);
        });
    }
  );
  qrScanner.start();
}
```

---

## 🗄️ Modèles de Données Ajoutés

### Message
```python
class Message(db.Model):
    id: Integer (Primary Key)
    sender_id: Integer (Foreign Key → User)
    recipient_id: Integer (Foreign Key → User)
    subject: String
    content: Text
    is_read: Boolean
    created_at: DateTime
```

### ChatMessage
```python
class ChatMessage(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key → User)
    message: Text
    is_bot_response: Boolean
    response: Text
    created_at: DateTime
```

---

## 📊 Améliorations par Rôle

### Admin
- ✅ Messagerie avec les autres admins
- ✅ Chatbot pour l'aide sur la gestion des utilisateurs
- ✅ Accès aux informations mobiles des actifs

### Responsable Patrimoine
- ✅ Messagerie avec les responsables de service
- ✅ Chatbot pour l'aide sur la gestion des actifs
- ✅ Accès aux informations mobiles des actifs

### Responsable Service
- ✅ Messagerie avec le responsable patrimoine
- ✅ Chatbot pour l'aide sur les demandes
- ✅ Accès aux informations mobiles des actifs

### Agent Maintenance
- ✅ Messagerie avec le responsable patrimoine
- ✅ Chatbot pour l'aide sur les interventions
- ✅ Accès aux informations mobiles des actifs via QR Code

### Auditeur
- ✅ Messagerie avec le responsable patrimoine
- ✅ Chatbot pour l'aide sur les rapports
- ✅ Accès aux informations mobiles des actifs

---

## 🧪 Tests

### Tester la Messagerie

```bash
# 1. Envoyer un message
curl -X POST http://localhost:5000/api/messages \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": 2,
    "subject": "Test",
    "content": "Ceci est un test"
  }'

# 2. Récupérer les messages
curl -X GET http://localhost:5000/api/messages \
  -H "Authorization: Bearer <token>"

# 3. Marquer comme lu
curl -X PUT http://localhost:5000/api/messages/1/read \
  -H "Authorization: Bearer <token>"
```

### Tester le Chatbot

```bash
# 1. Envoyer un message
curl -X POST http://localhost:5000/api/chatbot \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Comment créer un actif?"}'

# 2. Récupérer l'historique
curl -X GET http://localhost:5000/api/chatbot/history \
  -H "Authorization: Bearer <token>"
```

### Tester le QR Code

```bash
# Récupérer un actif par QR Code
curl -X GET http://localhost:5000/api/assets/qr/QR001
```

---

## 🔐 Sécurité

### Messagerie
- ✅ Authentification JWT requise
- ✅ Vérification du destinataire
- ✅ Chiffrement des données (recommandé)

### Chatbot
- ✅ Authentification JWT requise
- ✅ Réponses adaptées au rôle
- ✅ Historique sécurisé

### QR Code
- ✅ Pas d'authentification requise (accès public)
- ✅ Informations limitées (pas de données sensibles)
- ✅ Validation du QR Code

---

## 📈 Statistiques

| Fonctionnalité | Endpoints | Modèles | Cas d'Usage |
|---|---|---|---|
| Messagerie | 3 | 1 | 5+ |
| Chatbot | 2 | 1 | 10+ |
| QR Code | 1 | 0 | 5+ |

---

## 🎯 Prochaines Améliorations

- [ ] Notifications en temps réel (WebSocket)
- [ ] Chatbot avec IA (NLP)
- [ ] Chiffrement des messages
- [ ] Archivage des messages
- [ ] Groupes de discussion
- [ ] Pièces jointes aux messages
- [ ] Historique des QR Code scannés
- [ ] Statistiques de messagerie

---

## 📞 Support

Pour plus d'informations:
- Consultez `NEW_FEATURES.md` (ce fichier)
- Consultez `GUIDE_UTILISATION.md`
- Consultez `README.md`

---

**Dernière mise à jour**: Novembre 2024
