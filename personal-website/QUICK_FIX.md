# ⚡ Solution Rapide - Erreur 401

## 🔴 Problème

Vous recevez une erreur **401 (Unauthorized)** lors de la tentative de connexion.

```
127.0.0.1 - - [13/Nov/2025 12:59:50] "POST /api/auth/login HTTP/1.1" 401 -
```

---

## ✅ Solution en 1 Minute

### Étape 1: Arrêtez le Backend

Appuyez sur **CTRL+C** dans le terminal du backend.

### Étape 2: Initialisez la Base de Données

```bash
cd backend
python init_db.py
```

Vous devriez voir:

```
✓ Tables supprimées
✓ Tables créées
✓ 5 utilisateurs créés
✓ 12 actifs créés
✓ 5 maintenances créées
✓ 2 mouvements créés
✓ 3 alertes créées

==================================================
✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS
==================================================
```

### Étape 3: Redémarrez le Backend

```bash
python app.py
```

### Étape 4: Connectez-vous

Utilisez les identifiants:
- **Utilisateur:** `admin`
- **Mot de passe:** `admin123`

✅ **Ça marche!**

---

## 🎯 Pourquoi Cette Erreur?

La base de données n'était pas initialisée. Le script `init_db.py` crée:
- ✅ Les tables
- ✅ 5 utilisateurs de démonstration
- ✅ 12 actifs
- ✅ 5 maintenances
- ✅ 2 mouvements
- ✅ 3 alertes

Sans cela, aucun utilisateur n'existe et la connexion échoue.

---

## 🔑 5 Comptes de Démonstration

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| admin | admin123 | Admin |
| responsable | pass123 | Responsable Patrimoine |
| agent | pass123 | Agent Maintenance |
| auditeur | pass123 | Auditeur |
| service_chief | pass123 | Responsable Service |

---

## 📍 Où Créer de Nouveaux Utilisateurs?

### Option 1: Interface Web (Recommandé)

1. Connectez-vous en tant qu'**admin**
2. Cliquez sur **"Utilisateurs"**
3. Cliquez sur **"+ Ajouter un utilisateur"**
4. Remplissez le formulaire
5. Cliquez sur **"Créer"**

### Option 2: API

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ali_ben",
    "email": "ali@municipality.tn",
    "password": "SecurePass2024!",
    "full_name": "Ali Ben Ahmed",
    "role": "responsable_patrimoine"
  }'
```

---

## ✅ Checklist

- [ ] Backend arrêté
- [ ] `python init_db.py` exécuté
- [ ] Message "✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS" affiché
- [ ] Backend redémarré avec `python app.py`
- [ ] Connexion réussie avec admin/admin123

---

## 📞 Besoin d'Aide?

Consultez:
- **SETUP_GUIDE.md** - Guide complet de configuration
- **WHERE_IS_REGISTER.md** - Où créer des utilisateurs
- **ROLE_MANAGEMENT.md** - Gestion des rôles

---

**C'est tout! Ça devrait fonctionner maintenant! 🎉**
