#!/usr/bin/env python3
"""
Script pour mettre à jour le nom de l'utilisateur Sahar
"""

from app import app, db, User

def update_sahar():
    """Mettre à jour le nom de Sahar"""
    with app.app_context():
        try:
            # Trouver l'utilisateur sahar
            sahar = User.query.filter_by(username='sahar').first()
            if sahar:
                sahar.full_name = 'Sahar Ghribi'
                db.session.commit()
                print(f"✅ Nom mis à jour: {sahar.username} → {sahar.full_name}")
            else:
                print("❌ Utilisateur 'sahar' non trouvé")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Mise à jour du nom de Sahar...")
    update_sahar()
    print("✅ Terminé!")
