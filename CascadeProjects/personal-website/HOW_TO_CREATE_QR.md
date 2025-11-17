# 🎨 Comment Créer et Utiliser les Codes QR

## 🎯 Vue d'ensemble

Les codes QR sont des codes à barres 2D qui permettent d'accéder rapidement aux informations d'un actif en les scannant avec un téléphone.

---

## 📱 Codes QR Existants

Les codes QR sont **automatiquement créés** pour chaque actif lors de l'initialisation de la base de données.

### Liste des Codes QR

| Code QR | Actif | Catégorie |
|---------|-------|-----------|
| QR001 | Mairie Centrale | Bâtiment |
| QR002 | Centre de Santé | Bâtiment |
| QR003 | Bibliothèque Municipale | Bâtiment |
| QR004 | Ambulance 001 | Véhicule |
| QR005 | Camion Poubelle 001 | Véhicule |
| QR006 | Véhicule de Service 001 | Véhicule |
| QR007 | Serveur Informatique | Équipement |
| QR008 | Système de Climatisation | Équipement |
| QR009 | Groupe Électrogène | Équipement |
| QR010 | Bureau Directeur | Mobilier |
| QR011 | Chaises de Réunion | Mobilier |
| QR012 | Terrain Parc Municipal | Terrain |
| QR013 | Terrain Futur Stade | Terrain |

---

## 🖨️ Imprimer les Codes QR

### Méthode 1: Générer les Codes QR en Ligne

**Étape 1: Aller sur un Générateur QR**
- Allez à: https://www.qr-code-generator.com/
- Ou: https://www.qr-code-generator.fr/

**Étape 2: Entrer le Texte**
Pour chaque code QR, entrez le code:
- QR001
- QR002
- QR003
- etc.

**Étape 3: Générer l'Image**
1. Cliquez sur "Générer"
2. L'image QR s'affiche
3. Cliquez sur "Télécharger" ou "Imprimer"

**Étape 4: Imprimer**
1. Cliquez sur "Imprimer"
2. Sélectionnez votre imprimante
3. Cliquez sur "Imprimer"

### Méthode 2: Utiliser un Script Python

**Créer un fichier `generate_qr.py`:**

```python
import qrcode
import os

# Codes QR à générer
qr_codes = ['QR001', 'QR002', 'QR003', 'QR004', 'QR005', 'QR006', 
            'QR007', 'QR008', 'QR009', 'QR010', 'QR011', 'QR012', 'QR013']

# Créer un dossier pour les QR codes
os.makedirs('qr_codes', exist_ok=True)

# Générer chaque code QR
for code in qr_codes:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'qr_codes/{code}.png')
    print(f"✓ {code}.png créé")

print(f"\n✅ {len(qr_codes)} codes QR générés dans le dossier 'qr_codes'")
```

**Exécuter le script:**
```bash
pip install qrcode[pil]
python generate_qr.py
```

---

## 🏷️ Imprimer les Étiquettes

### Étape 1: Imprimer les Codes QR
1. Générez les codes QR (voir ci-dessus)
2. Imprimez-les sur du papier blanc

### Étape 2: Découper les Étiquettes
1. Découpez chaque code QR
2. Laissez une marge blanche autour

### Étape 3: Coller sur les Actifs
1. Nettoyez la surface de l'actif
2. Collez l'étiquette QR
3. Appuyez fermement pour bien coller

### Étape 4: Laminer (Optionnel)
1. Laminez l'étiquette pour la protéger
2. Cela prolonge la durée de vie

---

## 📱 Utiliser les Codes QR

### Avec un Smartphone

**Étape 1: Ouvrir le Scanner QR**
1. Ouvrez votre navigateur
2. Allez à: `http://localhost:3000/qr-scanner`
3. Ou scannez ce code QR avec votre téléphone

**Étape 2: Scanner le Code QR**
1. Pointez votre téléphone vers le code QR
2. Attendez que le code soit reconnu
3. Les informations s'affichent automatiquement

**Étape 3: Consulter les Informations**
1. Vous verrez les détails de l'actif
2. Nom, catégorie, localisation, etc.
3. Cliquez sur "Imprimer" pour imprimer

### Avec un Ordinateur

**Étape 1: Aller au Scanner QR**
1. Allez à: `http://localhost:3000/qr-scanner`

**Étape 2: Entrer le Code QR**
1. Cliquez dans le champ d'entrée
2. Tapez le code QR (ex: QR001)
3. Cliquez sur "Rechercher"

**Étape 3: Consulter les Informations**
1. Les détails de l'actif s'affichent
2. Cliquez sur "Imprimer" si nécessaire

---

## 🔧 Ajouter de Nouveaux Codes QR

### Méthode 1: Modifier init_db.py

**Étape 1: Ouvrir init_db.py**
```bash
nano backend/init_db.py
```

**Étape 2: Ajouter un Nouvel Actif**
```python
{
    'name': 'Nouvel Actif',
    'category': 'bâtiment',
    'description': 'Description',
    'acquisition_date': datetime(2024, 1, 1).date(),
    'acquisition_value': 100000,
    'current_value': 90000,
    'location': 'Localisation',
    'status': 'actif',
    'assigned_to': 'Responsable'
}
```

**Étape 3: Ajouter le Code QR**
```python
qr_codes = ['QR001', 'QR002', ..., 'QR014']  # Ajouter QR014
```

**Étape 4: Réinitialiser la BD**
```bash
python3 init_db.py
```

### Méthode 2: Ajouter via l'API

**Endpoint:**
```
POST /api/assets
```

**Body:**
```json
{
    "name": "Nouvel Actif",
    "category": "bâtiment",
    "description": "Description",
    "acquisition_date": "2024-01-01",
    "acquisition_value": 100000,
    "current_value": 90000,
    "location": "Localisation",
    "status": "actif",
    "assigned_to": "Responsable",
    "qr_code": "QR014"
}
```

---

## 🧪 Tester les Codes QR

### Test 1: Scanner QR001
1. Allez à `http://localhost:3000/qr-scanner`
2. Entrez: **QR001**
3. Cliquez sur "Rechercher"
4. Vous devriez voir: **Mairie Centrale**

### Test 2: Scanner QR004
1. Entrez: **QR004**
2. Cliquez sur "Rechercher"
3. Vous devriez voir: **Ambulance 001**

### Test 3: Scanner QR007
1. Entrez: **QR007**
2. Cliquez sur "Rechercher"
3. Vous devriez voir: **Serveur Informatique**

### Test 4: Code QR Invalide
1. Entrez: **QR999**
2. Cliquez sur "Rechercher"
3. Vous devriez voir: **"Actif non trouvé"**

---

## 📊 Informations Affichées

Quand vous scannez un code QR, vous verrez:

- ✅ **Nom**: Mairie Centrale
- ✅ **Catégorie**: Bâtiment
- ✅ **Localisation**: Centre-ville, Rue de la Liberté
- ✅ **Affecté à**: Mohamed Ben Ali
- ✅ **Date d'Acquisition**: 15/03/2015
- ✅ **Valeur d'Acquisition**: 500 000 DT
- ✅ **Valeur Actuelle**: 450 000 DT
- ✅ **Description**: Bâtiment administratif principal
- ✅ **Statut**: Actif

---

## 🎯 Cas d'Usage

### Cas 1: Technicien sur le Terrain
```
1. Arrive sur site
2. Ouvre le scanner QR sur son téléphone
3. Scanne le code QR de l'actif
4. Voit les informations (localisation, statut)
5. Effectue l'intervention
6. Enregistre le résultat
```

### Cas 2: Inspection Rapide
```
1. Inspecteur arrive
2. Ouvre le scanner QR
3. Scanne le code
4. Vérifie l'état de l'actif
5. Prend des photos
6. Enregistre les observations
```

### Cas 3: Vérification d'Inventaire
```
1. Agent d'inventaire arrive
2. Ouvre le scanner QR
3. Scanne chaque actif
4. Vérifie les informations
5. Confirme la présence
6. Enregistre les notes
```

---

## 📱 Générer des Codes QR Physiques

### Matériel Nécessaire
- Imprimante (couleur ou noir/blanc)
- Papier blanc
- Ciseaux
- Adhésif (sticker ou colle)
- Laminage (optionnel)

### Étapes
1. Générez les codes QR (voir ci-dessus)
2. Imprimez les codes QR
3. Découpez les étiquettes
4. Collez sur les actifs
5. Laminez pour protéger (optionnel)

---

## ✅ Checklist

- [ ] Codes QR générés
- [ ] Codes QR imprimés
- [ ] Étiquettes découpées
- [ ] Étiquettes collées sur les actifs
- [ ] Scanner QR accessible
- [ ] Codes QR scannables
- [ ] Informations affichées correctement
- [ ] Test de tous les codes QR
- [ ] Impression fonctionne

---

## 📞 Support

Pour plus d'informations:
- Consultez `QR_SCANNER_GUIDE.md`
- Consultez `TEST_NEW_FEATURES.md`
- Consultez `NEW_FEATURES.md`

---

**Bon scanning! 📱**

**Dernière mise à jour**: Novembre 2024
