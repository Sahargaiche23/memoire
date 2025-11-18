#!/usr/bin/env python3
"""
Script pour réinitialiser le mot de passe d'un utilisateur
"""

import sys
sys.path.insert(0, '.')

from app import app, db, User
from werkzeug.security import generate_password_hash

def reset_password(username, new_password):
    """Réinitialiser le mot de passe d'un utilisateur"""
    
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"❌ Utilisateur '{username}' non trouvé!")
            return False
        
        # Changer le mot de passe
        user.password_hash = generate_password_hash(new_password)
        
        try:
            db.session.commit()
            print(f"✅ Mot de passe de '{username}' réinitialisé avec succès!")
            print(f"   Nouveau mot de passe: {new_password}")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {e}")
            return False

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🔐 RÉINITIALISATION DE MOT DE PASSE")
    print("="*50 + "\n")
    
    username = input("Nom d'utilisateur: ").strip()
    new_password = input("Nouveau mot de passe: ").strip()
    
    if not username or not new_password:
        print("❌ Nom d'utilisateur et mot de passe requis!")
        sys.exit(1)
    
    reset_password(username, new_password)
    print()
