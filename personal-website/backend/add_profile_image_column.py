#!/usr/bin/env python3
"""
Ajouter la colonne profile_image à la table users
"""

import sys
sys.path.insert(0, '.')

from app import app, db

with app.app_context():
    print("\n" + "="*50)
    print("📊 MISE À JOUR DE LA BASE DE DONNÉES")
    print("="*50 + "\n")
    
    try:
        # Vérifier si la colonne existe déjà
        result = db.session.execute(db.text("PRAGMA table_info(users)")).fetchall()
        columns = [col[1] for col in result]
        
        if 'profile_image' in columns:
            print("✅ La colonne 'profile_image' existe déjà!")
        else:
            print("➕ Ajout de la colonne 'profile_image'...")
            db.session.execute(db.text("ALTER TABLE users ADD COLUMN profile_image VARCHAR(255)"))
            db.session.commit()
            print("✅ Colonne 'profile_image' ajoutée avec succès!")
        
        print("\n📋 Structure actuelle de la table users:")
        result = db.session.execute(db.text("PRAGMA table_info(users)")).fetchall()
        for col in result:
            print(f"   - {col[1]} ({col[2]})")
        
        print("\n✅ Mise à jour terminée!\n")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Erreur: {e}\n")
        sys.exit(1)
