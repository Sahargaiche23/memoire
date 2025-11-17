#!/usr/bin/env python3
"""
Test direct de l'API Maintenance
"""

import sys
sys.path.insert(0, '.')

from app import app, db, Maintenance
import requests

BACKEND_URL = "http://localhost:5000"

print("\n" + "="*70)
print("🧪 TEST API MAINTENANCE")
print("="*70 + "\n")

# Test 1: Login pour obtenir un token
print("📝 TEST 1: Connexion")
print("-" * 70)

try:
    response = requests.post(
        f"{BACKEND_URL}/api/auth/login",
        json={"username": "laila", "password": "test123"}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        print(f"✅ Connexion réussie!")
        print(f"   Token: {token[:30]}...")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"   Réponse: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

print()

# Test 2: Lire toutes les maintenances
print("📝 TEST 2: Lire les maintenances")
print("-" * 70)

try:
    response = requests.get(f"{BACKEND_URL}/api/maintenances")
    
    if response.status_code == 200:
        maintenances = response.json()
        print(f"✅ {len(maintenances)} maintenance(s) trouvée(s)")
        
        for m in maintenances[:3]:  # Afficher les 3 premières
            print(f"\n   ID: {m['id']}")
            print(f"   Type: {m['maintenance_type']}")
            print(f"   Description: '{m.get('description', '')}' {'(vide)' if not m.get('description') else ''}")
            print(f"   Coût: {m.get('cost', 'N/A')} DT")
            print(f"   Code: {m.get('code', 'N/A')}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"   Réponse: {response.text}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print()

# Test 3: Modifier une maintenance avec description
print("📝 TEST 3: Modifier une maintenance (ajouter description)")
print("-" * 70)

# Trouver la première maintenance
with app.app_context():
    first_maintenance = Maintenance.query.first()
    if first_maintenance:
        maintenance_id = first_maintenance.id
        print(f"Maintenance ID à modifier: {maintenance_id}")
        print(f"Description actuelle: '{first_maintenance.description or ''}'")
        
        # Modifier via API
        try:
            new_description = "TEST API - Description modifiée via script"
            response = requests.put(
                f"{BACKEND_URL}/api/maintenances/{maintenance_id}",
                json={
                    "asset_id": first_maintenance.asset_id,
                    "maintenance_type": first_maintenance.maintenance_type,
                    "scheduled_date": str(first_maintenance.scheduled_date),
                    "description": new_description,
                    "cost": first_maintenance.cost,
                    "status": first_maintenance.status
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                print(f"✅ Modification réussie!")
                data = response.json()
                print(f"   Nouvelle description: '{data['description']}'")
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"   Réponse: {response.text}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        # Vérifier en base de données
        db.session.refresh(first_maintenance)
        print(f"\n🗃️  Vérification en DB:")
        print(f"   Description en DB: '{first_maintenance.description or ''}'")
        
        if first_maintenance.description == new_description:
            print(f"   ✅ Description sauvegardée correctement!")
        else:
            print(f"   ❌ Description non sauvegardée!")
    else:
        print("❌ Aucune maintenance trouvée")

print()

# Test 4: Vérifier toutes les maintenances en DB
print("📝 TEST 4: État actuel en base de données")
print("-" * 70)

with app.app_context():
    maintenances = Maintenance.query.all()
    print(f"\n📊 {len(maintenances)} maintenance(s) en DB:\n")
    
    for m in maintenances:
        print(f"ID {m.id}: {m.maintenance_type}")
        print(f"  Description: '{m.description or '(vide)'}'")
        print(f"  Coût: {m.cost} DT")
        print(f"  Code: {m.code or 'N/A'}")
        print()

print("="*70)
print("✅ Tests terminés!")
print("="*70)
print()
