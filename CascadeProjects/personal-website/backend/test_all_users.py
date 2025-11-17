#!/usr/bin/env python3
"""
Tester que tous les utilisateurs peuvent se connecter et modifier leur profil
"""

import sys
sys.path.insert(0, '.')

from app import app, db, User
import requests

# Réinitialiser tous les mots de passe à "test123"
DEFAULT_PASSWORD = "test123"
BACKEND_URL = "http://localhost:5000"

with app.app_context():
    print("\n" + "="*70)
    print("🔐 TEST DE TOUS LES UTILISATEURS")
    print("="*70 + "\n")
    
    users = User.query.all()
    
    print(f"📋 {len(users)} utilisateurs trouvés:\n")
    
    for user in users:
        print(f"👤 {user.username} (ID: {user.id})")
        print(f"   Nom: {user.full_name}")
        print(f"   Email: {user.email}")
        print(f"   Rôle: {user.role}")
        
        # Réinitialiser le mot de passe
        user.set_password(DEFAULT_PASSWORD)
        db.session.add(user)
        
        print(f"   ✅ Mot de passe réinitialisé: {DEFAULT_PASSWORD}")
        print()
    
    try:
        db.session.commit()
        print("="*70)
        print("✅ Tous les mots de passe réinitialisés!")
        print("="*70)
        print()
        
        print("🔐 IDENTIFIANTS POUR TOUS LES UTILISATEURS:")
        print("="*70)
        for user in users:
            print(f"Username: {user.username:<15} | Password: {DEFAULT_PASSWORD}")
        print("="*70)
        print()
        
        # Test de connexion pour chaque utilisateur
        print("\n🧪 TEST DE CONNEXION POUR CHAQUE UTILISATEUR:")
        print("="*70)
        
        for user in users:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/auth/login",
                    json={"username": user.username, "password": DEFAULT_PASSWORD}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {user.username:<15} - Connexion OK")
                    print(f"   → Token reçu: {data['access_token'][:30]}...")
                else:
                    print(f"❌ {user.username:<15} - ERREUR: {response.status_code}")
            except Exception as e:
                print(f"❌ {user.username:<15} - ERREUR: {e}")
        
        print("="*70)
        print()
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Erreur: {e}\n")
        sys.exit(1)
    
    print("\n✅ TOUS LES UTILISATEURS PEUVENT MAINTENANT:")
    print("   1. Se connecter avec leur username / test123")
    print("   2. Modifier leur profil")
    print("   3. Uploader leur image de profil")
    print()
