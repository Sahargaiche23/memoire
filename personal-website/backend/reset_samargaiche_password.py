#!/usr/bin/env python3
"""
Réinitialiser le mot de passe de samargaiche
"""

import sys
sys.path.insert(0, '.')

from app import app, db, User
from werkzeug.security import generate_password_hash

NEW_PASSWORD = "test123"

with app.app_context():
    user = User.query.filter_by(username='samargaiche').first()
    
    if not user:
        print("❌ Utilisateur 'samargaiche' non trouvé!")
        sys.exit(1)
    
    print(f"🔍 Utilisateur trouvé:")
    print(f"   ID: {user.id}")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   QR Code: {user.qr_code}")
    print()
    
    # Changer le mot de passe
    user.password_hash = generate_password_hash(NEW_PASSWORD)
    
    try:
        db.session.commit()
        print(f"✅ Mot de passe réinitialisé avec succès!")
        print(f"   Nouveau mot de passe: {NEW_PASSWORD}")
        print()
        print(f"🔐 Vous pouvez maintenant vous connecter avec:")
        print(f"   Username: samargaiche")
        print(f"   Password: {NEW_PASSWORD}")
        print()
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur: {e}")
        sys.exit(1)
