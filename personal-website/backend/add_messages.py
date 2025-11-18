#!/usr/bin/env python3
from app import app, db, Message

with app.app_context():
    # Créer des messages de démonstration
    messages = [
        Message(
            sender_id=1,
            recipient_id=2,
            subject='Message',
            content='Bonjour, comment allez-vous?',
            is_read=False
        ),
        Message(
            sender_id=2,
            recipient_id=1,
            subject='Message',
            content='Bien, merci! Tout va bien.',
            is_read=False
        ),
        Message(
            sender_id=1,
            recipient_id=3,
            subject='Message',
            content='Pouvez-vous vérifier les actifs?',
            is_read=False
        ),
        Message(
            sender_id=3,
            recipient_id=1,
            subject='Message',
            content='Oui, je vais les vérifier maintenant.',
            is_read=False
        ),
        Message(
            sender_id=2,
            recipient_id=3,
            subject='Message',
            content='Salut Ahmed, comment ça va?',
            is_read=False
        ),
        Message(
            sender_id=3,
            recipient_id=2,
            subject='Message',
            content='Ça va bien, merci!',
            is_read=False
        ),
    ]
    
    db.session.add_all(messages)
    db.session.commit()
    
    print('✅ Messages de démonstration créés avec succès!')
    print(f'Total: {len(messages)} messages')
