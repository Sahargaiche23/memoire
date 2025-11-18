#!/usr/bin/env python3
"""
Script pour corriger les noms des utilisateurs dans la base de données
"""

from app import app, db, User, Message
from datetime import datetime

def fix_users():
    """Corriger les noms des utilisateurs"""
    with app.app_context():
        try:
            # Vérifier les utilisateurs existants
            users = User.query.all()
            print(f"Utilisateurs existants: {len(users)}")
            
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Full Name: {user.full_name}")
            
            # Mettre à jour les utilisateurs sans full_name
            users_to_update = [
                {'id': 1, 'full_name': 'Administrateur Système'},
                {'id': 2, 'full_name': 'Mohamed Ben Ali'},
                {'id': 3, 'full_name': 'Ahmed Khaled'},
                {'id': 4, 'full_name': 'Fatima Zahra'},
                {'id': 5, 'full_name': 'Omar Saïd'},
                {'id': 6, 'full_name': 'Sahar Ghribi'},
                {'id': 7, 'full_name': 'Amira Touati'},
                {'id': 8, 'full_name': 'Karim Mansouri'}
            ]
            
            updated_count = 0
            for user_data in users_to_update:
                user = User.query.get(user_data['id'])
                if user:
                    if not user.full_name or user.full_name.startswith('User'):
                        user.full_name = user_data['full_name']
                        updated_count += 1
                        print(f"✅ Mis à jour: {user.username} → {user.full_name}")
                    else:
                        print(f"✓ Déjà correct: {user.username} → {user.full_name}")
                else:
                    # Créer un nouvel utilisateur si nécessaire
                    new_user = User(
                        username=f"user{user_data['id']}",
                        email=f"user{user_data['id']}@municipality.tn",
                        full_name=user_data['full_name'],
                        role='user'
                    )
                    new_user.set_password('password123')
                    db.session.add(new_user)
                    updated_count += 1
                    print(f"✅ Créé: user{user_data['id']} → {user_data['full_name']}")
            
            # Sauvegarder les changements
            db.session.commit()
            print(f"\n✅ {updated_count} utilisateurs mis à jour avec succès!")
            
            # Vérifier les messages
            messages = Message.query.all()
            print(f"\nMessages dans la base: {len(messages)}")
            
            for msg in messages[:5]:  # Afficher les 5 premiers
                sender = User.query.get(msg.sender_id)
                recipient = User.query.get(msg.recipient_id)
                print(f"Message: {sender.full_name if sender else 'Unknown'} → {recipient.full_name if recipient else 'Unknown'}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Correction des noms d'utilisateurs...")
    fix_users()
    print("✅ Terminé!")
