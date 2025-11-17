# 🧪 TEST CRUD GROUPES - BACKEND ET FRONTEND

**Date:** 13 Novembre 2025  
**Heure:** 18:00

---

## 📋 ENDPOINTS BACKEND CRÉÉS

### 1. **GET /api/groups** - Récupérer tous les groupes
```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:5000/api/groups
```

### 2. **GET /api/groups/<id>** - Récupérer un groupe spécifique
```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:5000/api/groups/1
```

### 3. **PUT /api/groups/<id>** - Modifier un groupe
```bash
curl -X PUT -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Nouveau nom", "description": "Nouvelle description"}' \
  http://localhost:5000/api/groups/1
```

### 4. **DELETE /api/groups/<id>** - Supprimer un groupe
```bash
curl -X DELETE -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/groups/1
```

### 5. **POST /api/groups/<id>/leave** - Quitter un groupe
```bash
curl -X POST -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/groups/1/leave
```

---

## 🎯 TESTS FRONTEND

### TEST 1: Quitter un groupe
```
1. Allez à Messenger
2. Sélectionnez un groupe (ex: "Équipe Patrimoine")
3. Cliquez sur le menu contextuel (clic droit)
4. Sélectionnez "Quitter le groupe"
5. Confirmez
6. ✅ Le groupe disparaît de la liste
7. ✅ Appel à /api/groups/{id}/leave réussi
```

### TEST 2: Supprimer une conversation
```
1. Allez à Messenger
2. Sélectionnez une conversation
3. Cliquez sur le menu contextuel (clic droit)
4. Sélectionnez "Supprimer la conversation"
5. Confirmez
6. ✅ La conversation disparaît
7. ✅ Les messages associés sont supprimés
```

### TEST 3: Supprimer un message
```
1. Allez à Messenger
2. Sélectionnez une conversation
3. Survolez un message
4. Cliquez sur "🗑️" (Supprimer)
5. Confirmez
6. ✅ Le message disparaît
```

### TEST 4: Modifier un groupe (Backend)
```
1. Ouvrez Postman ou curl
2. Envoyez PUT /api/groups/1
3. Données: {"name": "Nouveau nom"}
4. ✅ Réponse: "Groupe mis à jour"
5. Vérifiez avec GET /api/groups/1
```

### TEST 5: Supprimer un groupe (Backend)
```
1. Ouvrez Postman ou curl
2. Envoyez DELETE /api/groups/1
3. ✅ Réponse: "Groupe supprimé"
4. Vérifiez avec GET /api/groups
5. Le groupe ne doit plus apparaître
```

---

## 📊 CHECKLIST

- [ ] Backend redémarré
- [ ] Frontend redémarré
- [ ] Endpoint GET /api/groups fonctionne
- [ ] Endpoint GET /api/groups/<id> fonctionne
- [ ] Endpoint PUT /api/groups/<id> fonctionne
- [ ] Endpoint DELETE /api/groups/<id> fonctionne
- [ ] Endpoint POST /api/groups/<id>/leave fonctionne
- [ ] Frontend: Quitter groupe fonctionne
- [ ] Frontend: Supprimer conversation fonctionne
- [ ] Frontend: Supprimer message fonctionne
- [ ] Les données se synchronisent correctement
- [ ] Pas d'erreurs dans la console

---

## 🔧 DÉPANNAGE

### Erreur 401 (Unauthorized)
```
- Vérifier le token JWT
- Vérifier l'en-tête Authorization
- Vérifier que le backend est démarré
```

### Erreur 404 (Not Found)
```
- Vérifier que le groupe existe
- Vérifier l'ID du groupe
- Vérifier que l'endpoint est correct
```

### Erreur 500 (Server Error)
```
- Vérifier les logs du backend
- Vérifier la base de données
- Vérifier que le modèle Group existe
```

---

## ✅ SUCCÈS

Si tous les tests passent, le CRUD est **100% FONCTIONNEL**!

---

**GUIDE DE TEST CRUD COMPLET! 🚀**
