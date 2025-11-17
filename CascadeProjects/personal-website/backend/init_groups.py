#!/usr/bin/env python3
"""
Script d'initialisation des groupes pour le système de messagerie
"""

from app import app, db, User, Group
from datetime import datetime

def init_groups():
    """Initialiser les groupes de test"""
    with app.app_context():
        try:
            # Créer les tables si elles n'existent pas
            db.create_all()
            
            # Vérifier si des groupes existent déjà
            if Group.query.count() > 0:
                print("✅ Des groupes existent déjà dans la base de données")
                return
            
            # Récupérer les utilisateurs existants
            users = User.query.all()
            if len(users) < 2:
                print("❌ Pas assez d'utilisateurs pour créer des groupes")
                return
            
            # Créer des groupes de test
            groups_data = [
                {
                    'name': 'Équipe Patrimoine',
                    'description': 'Groupe pour l\'équipe de gestion du patrimoine',
                    'created_by': users[0].id,
                    'members': users[:3] if len(users) >= 3 else users
                },
                {
                    'name': 'Maintenance',
                    'description': 'Groupe pour les équipes de maintenance',
                    'created_by': users[0].id,
                    'members': users[:2] if len(users) >= 2 else users
                },
                {
                    'name': 'Direction',
                    'description': 'Groupe pour la direction',
                    'created_by': users[0].id,
                    'members': users[:1]
                }
            ]
            
            # Créer les groupes
            for group_data in groups_data:
                group = Group(
                    name=group_data['name'],
                    description=group_data['description'],
                    created_by=group_data['created_by']
                )
                
                # Ajouter les membres
                for member in group_data['members']:
                    group.members.append(member)
                
                db.session.add(group)
            
            # Sauvegarder
            db.session.commit()
            
            print("✅ Groupes créés avec succès:")
            for group in Group.query.all():
                print(f"  - {group.name} ({len(group.members)} membres)")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Initialisation des groupes...")
    init_groups()
    print("✅ Terminé!")
