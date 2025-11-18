#!/usr/bin/env python3
from app import app, db, User, Asset, Maintenance, Movement, Alert, Message
from datetime import datetime, timedelta

def init_database():
    with app.app_context():
        # Supprimer les tables existantes
        db.drop_all()
        db.create_all()
        
        print("\n" + "="*50)
        print("✓ Tables supprimées et créées")
        
        # Créer les utilisateurs
        users_data = [
            {'username': 'admin', 'password': 'admin123', 'email': 'admin@patrimoine.tn', 'full_name': 'Administrateur Système', 'role': 'admin'},
            {'username': 'responsable', 'password': 'pass123', 'email': 'responsable@patrimoine.tn', 'full_name': 'Mohamed Ben Ali', 'role': 'responsable_patrimoine'},
            {'username': 'agent', 'password': 'pass123', 'email': 'agent@patrimoine.tn', 'full_name': 'Ahmed Khaled', 'role': 'agent_maintenance'},
            {'username': 'auditeur', 'password': 'pass123', 'email': 'auditeur@patrimoine.tn', 'full_name': 'Fatima Zahra', 'role': 'auditeur'},
            {'username': 'service_chief', 'password': 'pass123', 'email': 'chief@patrimoine.tn', 'full_name': 'Omar Saïd', 'role': 'responsable_service'},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ {len(users)} utilisateurs créés")
        
        # Créer les actifs
        assets_data = [
            {'name': 'Mairie Principale', 'category': 'bâtiment', 'description': 'Siège principal', 'acquisition_value': 500000},
            {'name': 'Salle de Réunion', 'category': 'bâtiment', 'description': 'Salle de conférence', 'acquisition_value': 50000},
            {'name': 'Garage Municipal', 'category': 'bâtiment', 'description': 'Garage pour véhicules', 'acquisition_value': 100000},
            {'name': 'Bus Municipal', 'category': 'véhicule', 'description': 'Transport public', 'acquisition_value': 80000},
            {'name': 'Voiture de Service', 'category': 'véhicule', 'description': 'Voiture administrative', 'acquisition_value': 25000},
            {'name': 'Ambulance', 'category': 'véhicule', 'description': 'Service médical', 'acquisition_value': 60000},
            {'name': 'Ordinateur Bureau', 'category': 'équipement', 'description': 'Équipement informatique', 'acquisition_value': 1500},
            {'name': 'Imprimante', 'category': 'équipement', 'description': 'Imprimante multifonction', 'acquisition_value': 800},
            {'name': 'Climatiseur', 'category': 'équipement', 'description': 'Système de climatisation', 'acquisition_value': 3000},
            {'name': 'Table de Réunion', 'category': 'mobilier', 'description': 'Mobilier de bureau', 'acquisition_value': 2000},
            {'name': 'Chaises de Bureau', 'category': 'mobilier', 'description': 'Ensemble de 10 chaises', 'acquisition_value': 1000},
            {'name': 'Armoires de Rangement', 'category': 'mobilier', 'description': 'Rangement documents', 'acquisition_value': 500},
            {'name': 'Terrain Municipal', 'category': 'terrain', 'description': 'Terrain pour développement', 'acquisition_value': 200000},
        ]
        
        assets = []
        for i, asset_data in enumerate(assets_data):
            asset = Asset(
                name=asset_data['name'],
                category=asset_data['category'],
                description=asset_data['description'],
                acquisition_date=datetime.now().date() - timedelta(days=365*i),
                acquisition_value=asset_data['acquisition_value'],
                current_value=asset_data['acquisition_value'] * 0.8,
                qr_code=f"QR{str(i+1).zfill(3)}"
            )
            assets.append(asset)
            db.session.add(asset)
        
        db.session.commit()
        print(f"✓ {len(assets)} actifs créés")
        
        # Créer les maintenances
        maintenances_data = [
            {'asset_id': 1, 'maintenance_type': 'préventive', 'description': 'Inspection annuelle'},
            {'asset_id': 4, 'maintenance_type': 'corrective', 'description': 'Réparation moteur'},
            {'asset_id': 7, 'maintenance_type': 'préventive', 'description': 'Maintenance informatique'},
            {'asset_id': 10, 'maintenance_type': 'corrective', 'description': 'Réparation chaise'},
            {'asset_id': 2, 'maintenance_type': 'préventive', 'description': 'Nettoyage'},
        ]
        
        maintenances = []
        for maint_data in maintenances_data:
            maintenance = Maintenance(
                asset_id=maint_data['asset_id'],
                maintenance_type=maint_data['maintenance_type'],
                description=maint_data['description'],
                scheduled_date=datetime.now().date() + timedelta(days=30),
                status='planifiée'
            )
            maintenances.append(maintenance)
            db.session.add(maintenance)
        
        db.session.commit()
        print(f"✓ {len(maintenances)} maintenances créées")
        
        # Créer les mouvements
        movements_data = [
            {'asset_id': 4, 'from_location': 'Garage', 'to_location': 'Centre Ville', 'reason': 'Affectation'},
            {'asset_id': 5, 'from_location': 'Parking', 'to_location': 'Garage', 'reason': 'Maintenance'},
        ]
        
        movements = []
        for move_data in movements_data:
            movement = Movement(
                asset_id=move_data['asset_id'],
                from_location=move_data['from_location'],
                to_location=move_data['to_location'],
                reason=move_data['reason'],
                created_by='Admin'
            )
            movements.append(movement)
            db.session.add(movement)
        
        db.session.commit()
        print(f"✓ {len(movements)} mouvements créés")
        
        # Créer les alertes
        alerts_data = [
            {'asset_id': 1, 'alert_type': 'maintenance', 'message': 'Maintenance urgente'},
            {'asset_id': 4, 'alert_type': 'maintenance', 'message': 'Révision prévue'},
            {'asset_id': 7, 'alert_type': 'maintenance', 'message': 'Mise à jour logicielle'},
        ]
        
        alerts = []
        for alert_data in alerts_data:
            alert = Alert(
                asset_id=alert_data['asset_id'],
                alert_type=alert_data['alert_type'],
                message=alert_data['message']
            )
            alerts.append(alert)
            db.session.add(alert)
        
        db.session.commit()
        print(f"✓ {len(alerts)} alertes créées")
        
        # Créer les messages
        messages_data = [
            {'sender_id': 1, 'recipient_id': 2, 'subject': 'Message', 'content': 'Bonjour, comment allez-vous?'},
            {'sender_id': 2, 'recipient_id': 1, 'subject': 'Message', 'content': 'Bien, merci!'},
            {'sender_id': 1, 'recipient_id': 3, 'subject': 'Message', 'content': 'Pouvez-vous vérifier les actifs?'},
            {'sender_id': 3, 'recipient_id': 1, 'subject': 'Message', 'content': 'Oui, je vais les vérifier!'},
            {'sender_id': 2, 'recipient_id': 3, 'subject': 'Message', 'content': 'Salut Ahmed!'},
            {'sender_id': 3, 'recipient_id': 2, 'subject': 'Message', 'content': 'Salut Mohamed!'},
        ]
        
        messages = []
        for msg_data in messages_data:
            message = Message(
                sender_id=msg_data['sender_id'],
                recipient_id=msg_data['recipient_id'],
                subject=msg_data['subject'],
                content=msg_data['content'],
                is_read=False
            )
            messages.append(message)
            db.session.add(message)
        
        db.session.commit()
        print(f"✓ {len(messages)} messages créés")
        
        print("\n" + "="*50)
        print("✅ BASE DE DONNÉES RÉINITIALISÉE AVEC SUCCÈS")
        print("="*50)
        print(f"\n📊 Statistiques:")
        print(f"   • Utilisateurs: {len(users)}")
        print(f"   • Actifs: {len(assets)}")
        print(f"   • Maintenances: {len(maintenances)}")
        print(f"   • Mouvements: {len(movements)}")
        print(f"   • Alertes: {len(alerts)}")
        print(f"   • Messages: {len(messages)}")
        print(f"\n🔐 Comptes de démonstration:")
        for user_data in users_data:
            print(f"   • {user_data['username']}: {user_data['password']} ({user_data['role']})")
        print("\n💡 Prochaines étapes:")
        print("   1. Démarrez le backend: python app.py")
        print("   2. Démarrez le frontend: npm start")
        print("   3. Ouvrez http://localhost:3000")
        print("   4. Connectez-vous avec les identifiants ci-dessus")
        print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    init_database()
