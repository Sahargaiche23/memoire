# 🗄️ GUIDE D'ACCÈS À VOTRE BASE DE DONNÉES

**Date:** 13 Novembre 2025  
**Heure:** 19:31

---

## 📍 LOCALISATION DE VOTRE BASE DE DONNÉES

**Fichier:** `/home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine.db`

**Type:** SQLite Database

---

## 📊 CONTENU DE VOTRE BASE DE DONNÉES

### **Statistiques Générales** ✅
```
📊 Utilisateurs   : 8
📊 Actifs         : 11
📊 Maintenances   : 6
📊 Groupes        : 3
📊 Messages       : 9
```

### **Utilisateurs (8)** ✅
```
1. admin           - Administrateur Système (admin)
2. responsable     - Mohamed Ben Ali (responsable_patrimoine)
3. agent           - Ahmed Khaled (agent_maintenance)
4. auditeur        - Fatima Zahra (auditeur)
5. service_chief   - Omar Saïd (responsable_service)
6. sahar           - Sahar Ghribi (responsable_patrimoine)
7. user7           - Amira Touatif (user)
8. samar           - samargaiche82@gmail.com (agent_maintenance)
```

### **Actifs par Catégorie (11)** ✅
```
🏢 Bâtiment (1)    : Garage Municipal (80,000€)
🪑 Mobilier (3)    : Table, Chaises, Armoires (2,800€)
🌍 Terrain (1)     : Terrain Municipal (160,000€)
🚗 Véhicule (3)    : Bus, Voiture, Ambulance (132,000€)
💻 Équipement (3)  : Ordinateur, Imprimante, Climatiseur (4,240€)
```

### **Maintenances (6)** ✅
```
✅ Préventives (3) : Inspection, Maintenance informatique, Nettoyage
🔧 Correctives (3) : Réparation moteur, Réparation chaise, Maintenance climatiseur
```

### **Groupes (3)** ✅
```
👥 Équipe Patrimoine (3 membres)
🔧 Maintenance (2 membres)
🏛️ Direction (1 membre)
```

---

## 🛠️ MÉTHODES D'ACCÈS À VOTRE BASE DE DONNÉES

### **1. Script Python Automatique** ✅ (Recommandé)
```bash
cd /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend
python3 view_database.py
```
**Avantages:**
- ✅ Vue complète et formatée
- ✅ Statistiques automatiques
- ✅ Facile à utiliser
- ✅ Pas besoin de connaître SQL

### **2. SQLite3 en Ligne de Commande** ✅
```bash
# Accéder à la base de données
sqlite3 /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine.db

# Commandes utiles:
.tables                          # Voir toutes les tables
.schema users                    # Voir la structure d'une table
SELECT * FROM users;             # Voir tous les utilisateurs
SELECT * FROM assets LIMIT 5;   # Voir 5 actifs
.quit                           # Quitter
```

### **3. Via l'Interface Web** ✅
```bash
# Démarrer le système
http://localhost:3000

# Pages pour voir les données:
/users        - Voir les utilisateurs
/assets       - Voir les actifs
/maintenance  - Voir les maintenances
/messenger    - Voir les groupes et messages
```

### **4. Via les APIs** ✅
```bash
# Obtenir un token JWT
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Utiliser le token pour accéder aux données
curl -H "Authorization: Bearer [TOKEN]" http://localhost:5000/api/users
curl -H "Authorization: Bearer [TOKEN]" http://localhost:5000/api/assets
curl -H "Authorization: Bearer [TOKEN]" http://localhost:5000/api/maintenances
curl -H "Authorization: Bearer [TOKEN]" http://localhost:5000/api/groups
```

---

## 📋 COMMANDES SQL UTILES

### **Voir les Tables**
```sql
.tables
```

### **Structure d'une Table**
```sql
.schema users
.schema assets
.schema maintenances
```

### **Requêtes Courantes**
```sql
-- Tous les utilisateurs
SELECT id, username, full_name, role FROM users;

-- Actifs par catégorie
SELECT category, COUNT(*) as count, SUM(current_value) as total_value 
FROM assets GROUP BY category;

-- Maintenances en cours
SELECT m.id, a.name, m.maintenance_type, m.scheduled_date, m.status 
FROM maintenances m 
LEFT JOIN assets a ON m.asset_id = a.id 
WHERE m.status = 'planifiée';

-- Messages récents
SELECT m.id, u1.full_name as sender, u2.full_name as recipient, 
       m.content, m.created_at 
FROM messages m 
LEFT JOIN users u1 ON m.sender_id = u1.id 
LEFT JOIN users u2 ON m.recipient_id = u2.id 
ORDER BY m.created_at DESC LIMIT 5;

-- Membres des groupes
SELECT g.name as groupe, u.full_name as membre 
FROM groups g 
JOIN group_members gm ON g.id = gm.group_id 
JOIN users u ON gm.user_id = u.id 
ORDER BY g.name;
```

---

## 🔧 OUTILS GRAPHIQUES (Optionnels)

### **DB Browser for SQLite** (Interface Graphique)
```bash
# Installation sur Ubuntu/Debian
sudo apt install sqlitebrowser

# Utilisation
sqlitebrowser /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine.db
```

### **DBeaver** (Outil Professionnel)
```bash
# Télécharger depuis: https://dbeaver.io/
# Connecter à votre fichier SQLite
```

---

## 📊 SAUVEGARDE DE VOTRE BASE DE DONNÉES

### **Sauvegarde Simple**
```bash
cp /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine.db \
   /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine_backup_$(date +%Y%m%d).db
```

### **Export SQL**
```bash
sqlite3 /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine.db \
  .dump > patrimoine_backup.sql
```

---

## 🚀 ACCÈS RAPIDE

### **Commande Rapide pour Voir Toute la Base**
```bash
cd /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend && python3 view_database.py
```

### **Commande Rapide pour SQLite**
```bash
sqlite3 /home/sahar/Bureau/ERPM2/CascadeProjects/personal-website/backend/instance/patrimoine.db
```

---

## ✅ RÉSUMÉ

**Votre base de données contient:**
- ✅ **8 utilisateurs** avec différents rôles
- ✅ **11 actifs** d'une valeur totale de ~379,040€
- ✅ **6 maintenances** planifiées
- ✅ **3 groupes** de messagerie
- ✅ **9 messages** échangés

**Méthodes d'accès recommandées:**
1. 🥇 **Script Python** (`python3 view_database.py`) - Le plus facile
2. 🥈 **Interface Web** (`http://localhost:3000`) - Le plus visuel
3. 🥉 **SQLite3** - Le plus flexible

---

**VOTRE BASE DE DONNÉES EST COMPLÈTE ET FONCTIONNELLE! 🎉**
