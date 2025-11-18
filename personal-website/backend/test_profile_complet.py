#!/usr/bin/env python3
"""
Test complet du système de profil:
- Modification de profil
- Upload d'image
- Vérification en base de données
"""

import sys
import os
import requests
import time
from io import BytesIO
from PIL import Image

sys.path.insert(0, '.')
from app import app, db, User

BACKEND_URL = "http://localhost:5000"
TEST_USER = "sahar"
TEST_PASSWORD = "test123"

def create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (200, 200), color='blue')
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer

print("\n" + "="*70)
print("🧪 TEST COMPLET - PROFIL ET UPLOAD D'IMAGE")
print("="*70 + "\n")

# Test 1: Connexion
print("📝 TEST 1: CONNEXION")
print("-" * 70)

try:
    response = requests.post(
        f"{BACKEND_URL}/api/auth/login",
        json={"username": TEST_USER, "password": TEST_PASSWORD}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        user_data = data['user']
        user_id = user_data['id']
        
        print(f"✅ Connexion réussie!")
        print(f"   User ID: {user_id}")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Nom: {user_data['full_name']}")
        print(f"   QR Code: {user_data['qr_code']}")
        print(f"   Image actuelle: {user_data.get('profile_image', 'Aucune')}")
        print(f"   Token: {token[:30]}...")
    else:
        print(f"❌ Erreur de connexion: {response.status_code}")
        print(f"   Réponse: {response.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

print()

# Test 2: Modification du profil
print("📝 TEST 2: MODIFICATION DU PROFIL")
print("-" * 70)

new_name = f"Test User {int(time.time())}"
new_email = f"test{int(time.time())}@example.com"

try:
    response = requests.put(
        f"{BACKEND_URL}/api/users/{user_id}",
        json={
            "full_name": new_name,
            "email": new_email
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Modification réussie!")
        print(f"   Nouveau nom: {data['user']['full_name']}")
        print(f"   Nouvel email: {data['user']['email']}")
        
        # Vérification en base de données
        with app.app_context():
            user = db.session.get(User, user_id)
            if user.full_name == new_name and user.email == new_email:
                print(f"✅ Données vérifiées en base de données!")
            else:
                print(f"❌ Données en DB ne correspondent pas!")
                print(f"   DB - Nom: {user.full_name}")
                print(f"   DB - Email: {user.email}")
    else:
        print(f"❌ Erreur modification: {response.status_code}")
        print(f"   Réponse: {response.text}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print()

# Test 3: Upload d'image
print("📝 TEST 3: UPLOAD D'IMAGE DE PROFIL")
print("-" * 70)

try:
    # Créer une image de test
    test_image = create_test_image()
    
    response = requests.post(
        f"{BACKEND_URL}/api/users/{user_id}/profile-image",
        files={'file': ('test_profile.png', test_image, 'image/png')},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload réussi!")
        print(f"   Fichier: {data['filename']}")
        print(f"   URL: {data['url']}")
        
        # Vérification en base de données
        with app.app_context():
            user = db.session.get(User, user_id)
            if user.profile_image:
                print(f"✅ Chemin sauvegardé en base de données!")
                print(f"   DB - Image: {user.profile_image}")
                
                # Vérifier que le fichier existe
                upload_path = os.path.join(os.path.dirname(__file__), 'uploads', user.profile_image)
                if os.path.exists(upload_path):
                    size = os.path.getsize(upload_path)
                    print(f"✅ Fichier physique existe!")
                    print(f"   Chemin: {upload_path}")
                    print(f"   Taille: {size} bytes")
                else:
                    print(f"❌ Fichier physique introuvable!")
            else:
                print(f"❌ Chemin d'image non sauvegardé en DB!")
    else:
        print(f"❌ Erreur upload: {response.status_code}")
        print(f"   Réponse: {response.text}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print()

# Test 4: Récupération des données après modifications
print("📝 TEST 4: VÉRIFICATION FINALE")
print("-" * 70)

try:
    response = requests.post(
        f"{BACKEND_URL}/api/auth/login",
        json={"username": TEST_USER, "password": TEST_PASSWORD}
    )
    
    if response.status_code == 200:
        data = response.json()
        user_data = data['user']
        
        print(f"✅ Reconnexion réussie!")
        print(f"   Nom: {user_data['full_name']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Image: {user_data.get('profile_image', 'Aucune')}")
        
        # Vérifier que c'est bien les nouvelles données
        if user_data['full_name'] == new_name:
            print(f"✅ Le nom a été persisté!")
        else:
            print(f"❌ Le nom n'a pas été persisté!")
            
        if user_data['email'] == new_email:
            print(f"✅ L'email a été persisté!")
        else:
            print(f"❌ L'email n'a pas été persisté!")
            
        if user_data.get('profile_image'):
            print(f"✅ L'image a été persistée!")
        else:
            print(f"⚠️  Pas d'image de profil")
    else:
        print(f"❌ Erreur reconnexion: {response.status_code}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print()
print("="*70)
print("📊 RÉSUMÉ DES TESTS")
print("="*70)

with app.app_context():
    user = db.session.get(User, user_id)
    print(f"\n🗃️  ÉTAT ACTUEL EN BASE DE DONNÉES:")
    print(f"   ID: {user.id}")
    print(f"   Username: {user.username}")
    print(f"   Nom complet: {user.full_name}")
    print(f"   Email: {user.email}")
    print(f"   Rôle: {user.role}")
    print(f"   QR Code: {user.qr_code}")
    print(f"   Image de profil: {user.profile_image or 'Aucune'}")
    print(f"   Créé le: {user.created_at}")

print("\n✅ Tests terminés!\n")
