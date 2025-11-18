#!/usr/bin/env python3
"""
Script pour nettoyer les messages de groupe mal placés
"""
from app import app, db, Message, Group

with app.app_context():
    # Récupérer tous les IDs de groupes
    group_ids = [g.id for g in Group.query.all()]
    print(f"📊 IDs de groupes trouvés: {group_ids}")
    
    # Trouver les messages de groupe (subject contient "Message groupe:")
    group_messages = Message.query.filter(
        Message.subject.like('%Message groupe:%')
    ).all()
    
    print(f"📨 {len(group_messages)} messages de groupe trouvés")
    
    for msg in group_messages:
        print(f"  - ID: {msg.id}, Recipient: {msg.recipient_id}, Subject: {msg.subject}")
    
    # Option: Supprimer ces messages (décommenter si nécessaire)
    # if input("\n⚠️  Supprimer ces messages? (oui/non): ").lower() == 'oui':
    #     for msg in group_messages:
    #         db.session.delete(msg)
    #     db.session.commit()
    #     print(f"✅ {len(group_messages)} messages supprimés")
    # else:
    #     print("❌ Annulé")
