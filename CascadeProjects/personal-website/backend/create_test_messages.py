#!/usr/bin/env python3
"""
Script pour créer des messages de test avec de vrais noms
"""

from app import app, db, User, Message
from datetime import datetime

def create_test_messages():
    """Créer des messages de test"""
    with app.app_context():
        try:
            # Récupérer les utilisateurs
            users = User.query.all()
            print(f"Utilisateurs disponibles: {len(users)}")
            
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Full Name: {user.full_name}")
            
            # Créer des messages de test
            messages_data = [
                {
                    'sender_id': 1,  # Administrateur Système
                    'recipient_id': 6,  # Sahar Ghribi
                    'content': 'Bonjour Sahar, comment allez-vous?',
                    'subject': 'Salutations'
                },
                {
                    'sender_id': 2,  # Mohamed Ben Ali
                    'recipient_id': 6,  # Sahar Ghribi
                    'content': 'Pouvez-vous vérifier les actifs?',
                    'subject': 'Vérification'
                },
                {
                    'sender_id': 3,  # Ahmed Khaled
                    'recipient_id': 6,  # Sahar Ghribi
                    'content': 'La maintenance est terminée',
                    'subject': 'Maintenance'
                },
                {
                    'sender_id': 4,  # Fatima Zahra
                    'recipient_id': 6,  # Sahar Ghribi
                    'content': 'Rapport d\'audit prêt',
                    'subject': 'Audit'
                },
                {
                    'sender_id': 7,  # Amira Touati
                    'recipient_id': 6,  # Sahar Ghribi
                    'content': 'Réunion prévue demain',
                    'subject': 'Réunion'
                }
            ]
            
            # Supprimer les anciens messages de test
            Message.query.filter_by(recipient_id=6).delete()
            
            created_count = 0
            for msg_data in messages_data:
                # Vérifier que les utilisateurs existent
                sender = User.query.get(msg_data['sender_id'])
                recipient = User.query.get(msg_data['recipient_id'])
                
                if sender and recipient:
                    message = Message(
                        sender_id=msg_data['sender_id'],
                        recipient_id=msg_data['recipient_id'],
                        content=msg_data['content'],
                        subject=msg_data['subject']
                    )
                    db.session.add(message)
                    created_count += 1
                    print(f"✅ Message créé: {sender.full_name} → {recipient.full_name}")
                else:
                    print(f"❌ Utilisateur manquant: sender={msg_data['sender_id']}, recipient={msg_data['recipient_id']}")
            
            # Sauvegarder
            db.session.commit()
            print(f"\n✅ {created_count} messages créés avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Création de messages de test...")
    create_test_messages()
    print("✅ Terminé!")
