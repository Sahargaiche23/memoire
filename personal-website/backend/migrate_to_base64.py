#!/usr/bin/env python3
"""
Migration: Convertir profile_image de VARCHAR à TEXT pour Base64
"""

import sys
import os
sys.path.insert(0, '.')

from app import app, db, User

print("\n" + "="*70)
print("🔄 MIGRATION - Images Base64")
print("="*70 + "\n")

with app.app_context():
    try:
        # SQLite ne supporte pas ALTER COLUMN, donc on doit:
        # 1. Créer une nouvelle table temporaire
        # 2. Copier les données
        # 3. Supprimer l'ancienne table
        # 4. Renommer la nouvelle table
        
        print("📝 Étape 1: Sauvegarde des données actuelles...")
        
        # Lire toutes les données utilisateurs
        users_data = []
        users = User.query.all()
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password_hash': user.password_hash,
                'role': user.role,
                'full_name': user.full_name,
                'qr_code': user.qr_code,
                'profile_image': user.profile_image,
                'created_at': user.created_at
            })
        
        print(f"✅ {len(users_data)} utilisateurs sauvegardés")
        
        print("\n📝 Étape 2: Recréation de la table avec TEXT...")
        
        # Supprimer et recréer la table
        db.session.execute(db.text("DROP TABLE IF EXISTS users_temp;"))
        db.session.execute(db.text("""
            CREATE TABLE users_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50),
                full_name VARCHAR(120),
                qr_code VARCHAR(255),
                profile_image TEXT,
                created_at DATETIME
            );
        """))
        
        print("✅ Nouvelle structure créée")
        
        print("\n📝 Étape 3: Restauration des données...")
        
        # Restaurer les données
        for user_data in users_data:
            # Convertir les anciens chemins de fichiers en None
            # Car maintenant on stocke du Base64
            profile_image = user_data['profile_image']
            if profile_image and not profile_image.startswith('data:'):
                print(f"   ⚠️  {user_data['username']}: Ancien format de fichier détecté, réinitialisé")
                profile_image = None
            
            db.session.execute(db.text("""
                INSERT INTO users_temp 
                (id, username, email, password_hash, role, full_name, qr_code, profile_image, created_at)
                VALUES 
                (:id, :username, :email, :password_hash, :role, :full_name, :qr_code, :profile_image, :created_at)
            """), {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'password_hash': user_data['password_hash'],
                'role': user_data['role'],
                'full_name': user_data['full_name'],
                'qr_code': user_data['qr_code'],
                'profile_image': profile_image,
                'created_at': user_data['created_at']
            })
        
        print(f"✅ {len(users_data)} utilisateurs restaurés")
        
        print("\n📝 Étape 4: Remplacement de la table...")
        
        db.session.execute(db.text("DROP TABLE users;"))
        db.session.execute(db.text("ALTER TABLE users_temp RENAME TO users;"))
        
        db.session.commit()
        
        print("✅ Migration terminée!")
        
        print("\n📊 VÉRIFICATION:")
        print("-" * 70)
        
        # Vérifier la structure
        result = db.session.execute(db.text("PRAGMA table_info(users);")).fetchall()
        for col in result:
            print(f"   - {col[1]:<20} {col[2]}")
        
        print("\n📋 UTILISATEURS:")
        print("-" * 70)
        users = User.query.all()
        for user in users:
            has_image = "✅" if user.profile_image else "❌"
            image_type = "Base64" if (user.profile_image and user.profile_image.startswith('data:')) else "Aucune"
            print(f"   {has_image} {user.username:<15} - Image: {image_type}")
        
        print("\n" + "="*70)
        print("✅ MIGRATION RÉUSSIE!")
        print("="*70)
        print("\n💡 Les anciennes images de profil (fichiers) ont été réinitialisées.")
        print("   Les utilisateurs devront uploader à nouveau leurs images.")
        print("   Les nouvelles images seront stockées en Base64 dans la DB.\n")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Erreur: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
