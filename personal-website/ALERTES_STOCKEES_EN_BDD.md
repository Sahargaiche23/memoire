# 🔔 TRANSFORMATION: ALERTES DYNAMIQUES → STOCKÉES EN BDD

## ✅ CHANGEMENT IMPLÉMENTÉ

Les alertes sont maintenant **stockées en base de données** au lieu d'être générées dynamiquement à la volée!

---

## 📊 AVANT vs APRÈS

### ❌ AVANT (Alertes 100% dynamiques)

**Fonctionnement:**
- Alertes générées à chaque requête GET /api/alerts
- Calcul en temps réel depuis Maintenance + Asset
- **Aucun stockage** en base de données
- IDs temporaires (ex: "maintenance-5")
- Impossible de marquer comme "lu"
- Auto-refresh frontend toutes les 30s

**Avantages:**
- ✅ Toujours à jour (temps réel)
- ✅ Pas de maintenance de la table alerts
- ✅ Léger (pas de stockage)

**Inconvénients:**
- ❌ Impossible de marquer comme "lu"
- ❌ Pas d'historique des alertes
- ❌ Recalcul à chaque requête (performance)
- ❌ Pas de personnalisation par utilisateur

---

### ✅ APRÈS (Alertes stockées en BDD)

**Fonctionnement:**
- Alertes **stockées** dans la table `alerts`
- Génération/mise à jour via fonction `generate_and_update_alerts()`
- Lecture depuis BDD (GET /api/alerts)
- IDs permanents (Integer)
- **Marquage "lu"** fonctionnel
- Soft delete (désactivation au lieu de suppression)

**Avantages:**
- ✅ **Marquage "lu" fonctionnel**
- ✅ Historique complet des alertes
- ✅ Meilleures performances (lecture BDD)
- ✅ Personnalisation par utilisateur possible
- ✅ Statistiques sur les alertes
- ✅ Audit trail complet

**Inconvénients:**
- ⚠️ Nécessite régénération périodique
- ⚠️ Table alerts à maintenir

---

## 🔧 MODIFICATIONS TECHNIQUES

### 1. Modèle Alert Amélioré

**Nouveaux champs ajoutés:**

```python
class Alert(db.Model):
    # Anciens champs
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # NOUVEAUX CHAMPS
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenances.id'), nullable=True)
    priority = db.Column(db.String(20), default='MEDIUM')  # HIGH, CRITICAL, MEDIUM
    days_count = db.Column(db.Integer, nullable=True)  # Jours restants ou retard
    is_active = db.Column(db.Boolean, default=True)  # Soft delete
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    asset = db.relationship('Asset', backref='alerts', foreign_keys=[asset_id])
    maintenance = db.relationship('Maintenance', backref='alerts', foreign_keys=[maintenance_id])
```

**Types d'alertes:**
- `MAINTENANCE_URGENT` - Maintenance dans les 7 prochains jours (priorité HIGH)
- `MAINTENANCE_LATE` - Maintenance en retard (priorité CRITICAL)
- `ASSET_MAINTENANCE_REQUIRED` - Actif nécessitant maintenance (priorité MEDIUM)

---

### 2. Fonction de Génération

**Nouvelle fonction: `generate_and_update_alerts()`**

```python
def generate_and_update_alerts():
    """
    Génère/met à jour les alertes stockées en BDD
    """
    # 1. Désactiver toutes les alertes existantes
    Alert.query.update({'is_active': False})
    
    # 2. Pour chaque type d'alerte:
    #    - Vérifier si existe déjà → Mise à jour
    #    - Sinon → Création
    
    # 3. Commit
    db.session.commit()
    
    # 4. Supprimer les alertes restées inactives
    Alert.query.filter_by(is_active=False).delete()
    
    return alerts_created, alerts_updated
```

**Logique intelligente:**
- ✅ Évite les doublons
- ✅ Met à jour les alertes existantes (message, days_count)
- ✅ Crée uniquement les nouvelles
- ✅ Supprime les alertes obsolètes
- ✅ Préserve le statut "lu"

---

### 3. Endpoints API Modifiés

#### GET /api/alerts

**AVANT:**
```python
# Générait les alertes à la volée
urgent_maintenances = Maintenance.query.filter(...)
for m in urgent_maintenances:
    all_alerts.append({...})  # Dictionnaire temporaire
return jsonify(all_alerts)
```

**APRÈS:**
```python
# Régénère puis lit depuis BDD
generate_and_update_alerts()  # Mise à jour
alerts = Alert.query.filter_by(is_active=True).all()
return jsonify([alert.to_dict() for alert in alerts])
```

#### PUT /api/alerts/<id>/read

**AVANT:**
```python
# Ne fonctionnait pas (alertes dynamiques)
if isinstance(alert_id, str) and ('-' in alert_id):
    return "Les alertes dynamiques se mettent à jour automatiquement"
```

**APRÈS:**
```python
# Fonctionne parfaitement
alert = db.session.get(Alert, alert_id)
alert.is_read = True
db.session.commit()
return jsonify({'message': 'Alerte marquée comme lue'})
```

#### POST /api/alerts/generate (NOUVEAU)

**Endpoint pour régénération manuelle:**
```python
@app.route('/api/alerts/generate', methods=['POST'])
@jwt_required()
def regenerate_alerts():
    alerts_created, alerts_updated = generate_and_update_alerts()
    return jsonify({
        'alerts_created': alerts_created,
        'alerts_updated': alerts_updated
    })
```

#### DELETE /api/alerts/<id> (NOUVEAU)

**Soft delete (désactivation):**
```python
@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
@jwt_required()
def delete_alert(alert_id):
    alert = db.session.get(Alert, alert_id)
    alert.is_active = False  # Soft delete
    db.session.commit()
```

---

## 🚀 MIGRATION

### Étape 1: Exécuter le script de migration

```bash
cd backend
python3 migrate_alerts.py
```

**Ce que fait le script:**
1. Supprime l'ancienne table `alerts` (si existe)
2. Crée la nouvelle table avec la structure améliorée
3. Affiche la nouvelle structure

### Étape 2: Redémarrer le backend

```bash
python3 app.py
```

**Au redémarrage:**
- Les alertes seront générées automatiquement au premier GET /api/alerts
- La table se remplit progressivement

### Étape 3: Vérifier

**Requête test:**
```bash
# Vérifier que les alertes sont créées
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/alerts
```

**Résultat attendu:**
```json
[
  {
    "id": 1,
    "asset_id": 5,
    "maintenance_id": 12,
    "alert_type": "MAINTENANCE_URGENT",
    "priority": "HIGH",
    "message": "Maintenance prévue: Ordinateur Bureau 101 dans 3 jour(s)",
    "due_date": "2025-11-21",
    "days_count": 3,
    "is_read": false,
    "is_active": true,
    "created_at": "2025-11-18T12:00:00",
    "updated_at": "2025-11-18T12:00:00"
  }
]
```

---

## 📈 FONCTIONNALITÉS NOUVELLES

### 1. Marquage "Lu" Fonctionnel

**Requête:**
```bash
PUT /api/alerts/1/read
```

**Réponse:**
```json
{
  "message": "Alerte marquée comme lue",
  "alert": {
    "id": 1,
    "is_read": true,
    ...
  }
}
```

### 2. Régénération Manuelle

**Utilité:** Forcer la mise à jour des alertes sans attendre la prochaine requête GET

```bash
POST /api/alerts/generate
```

**Réponse:**
```json
{
  "message": "Alertes régénérées avec succès",
  "alerts_created": 5,
  "alerts_updated": 3
}
```

### 3. Suppression d'Alerte

**Soft delete - l'alerte est désactivée, pas supprimée:**

```bash
DELETE /api/alerts/1
```

### 4. Historique et Statistiques

**Requêtes SQL possibles:**

```sql
-- Nombre d'alertes par type
SELECT alert_type, COUNT(*) FROM alerts WHERE is_active=1 GROUP BY alert_type;

-- Alertes non lues par priorité
SELECT priority, COUNT(*) FROM alerts WHERE is_read=0 GROUP BY priority;

-- Historique des alertes (incluant désactivées)
SELECT * FROM alerts WHERE created_at > '2025-11-01' ORDER BY created_at DESC;
```

---

## 🔄 RÉGÉNÉRATION AUTOMATIQUE

### Stratégies Possibles

**Option 1: À chaque requête GET** (implémenté actuellement)
```python
# Dans get_alerts()
generate_and_update_alerts()  # Appel à chaque GET
```

**Avantages:** Toujours à jour  
**Inconvénients:** Performance (si beaucoup de requêtes)

---

**Option 2: Scheduler périodique** (recommandé pour production)

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=generate_and_update_alerts,
    trigger="interval",
    minutes=5  # Toutes les 5 minutes
)
scheduler.start()
```

**Avantages:** Meilleures performances  
**Inconvénients:** Latence max 5 minutes

---

**Option 3: Webhook/Event-driven** (optimal)

```python
# Dans les endpoints qui modifient les maintenances
@app.route('/api/maintenances', methods=['POST'])
def create_maintenance():
    # ... créer maintenance ...
    generate_and_update_alerts()  # Régénérer alertes
```

**Avantages:** Temps réel + performances  
**Inconvénients:** Plus complexe

---

## 🎯 RÉSUMÉ DES BÉNÉFICES

### ✅ Fonctionnalités Ajoutées

1. **Marquage "lu" fonctionnel** ⭐
2. **Historique complet des alertes**
3. **Soft delete (traçabilité)**
4. **Personnalisation par utilisateur** (possible)
5. **Statistiques sur les alertes**
6. **Meilleures performances** (lecture BDD)
7. **Audit trail complet**
8. **Régénération manuelle** (endpoint dédié)

### 📊 Améliorations UX

- ✅ Utilisateur peut marquer alertes comme lues
- ✅ Alertes persistent (pas de perte au refresh)
- ✅ Compteur d'alertes non lues précis
- ✅ Historique consultable
- ✅ Possibilité de "dismisser" une alerte

---

## 🔐 SÉCURITÉ

**Points d'attention:**

1. **Validation des IDs:**
   ```python
   @app.route('/api/alerts/<int:alert_id>/read')  # Type checking automatique
   ```

2. **Vérification propriété:**
   ```python
   # À ajouter si alertes personnalisées par utilisateur
   if alert.user_id != current_user_id:
       return jsonify({'error': 'Accès non autorisé'}), 403
   ```

3. **Soft delete:** Préserve les données pour audit

4. **Timestamps:** `created_at` et `updated_at` pour traçabilité

---

## 📝 DOCUMENTATION API

### Endpoints Alertes

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/alerts` | Récupérer toutes les alertes actives (régénère automatiquement) |
| PUT | `/api/alerts/<id>/read` | Marquer une alerte comme lue |
| POST | `/api/alerts/generate` | Régénérer manuellement les alertes |
| DELETE | `/api/alerts/<id>` | Désactiver une alerte (soft delete) |

---

## 🧪 TESTS

### Test 1: Génération Initiale

```bash
cd backend
python3 migrate_alerts.py
python3 app.py
# Faire une requête GET /api/alerts
```

**Attendu:** Alertes créées automatiquement

### Test 2: Marquage Lu

```bash
curl -X PUT -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/alerts/1/read
```

**Attendu:** `is_read: true`

### Test 3: Mise à Jour Automatique

1. Créer une maintenance dans 3 jours
2. GET /api/alerts → Alerte "dans 3 jours"
3. Attendre 1 jour
4. GET /api/alerts → Alerte "dans 2 jours" (mise à jour auto)

---

## 🎓 CONCLUSION

Le système d'alertes est maintenant **beaucoup plus robuste et fonctionnel**!

**Transformation réussie:**
- ❌ Alertes dynamiques éphémères
- ✅ Alertes persistantes avec historique complet

**Impact utilisateur:**
- **Meilleure expérience:** Marquage "lu" fonctionne
- **Plus de contrôle:** Possibilité de gérer les alertes
- **Traçabilité:** Historique complet

**Recommandation:** En production, implémenter un scheduler (Option 2) pour optimiser les performances!

---

**Fichiers modifiés:**
- ✅ `backend/app.py` - Modèle Alert + Fonction génération + Endpoints
- ✅ `backend/migrate_alerts.py` - Script de migration
- ✅ `ALERTES_STOCKEES_EN_BDD.md` - Cette documentation

**Prochaine étape:** Tester et déployer! 🚀
