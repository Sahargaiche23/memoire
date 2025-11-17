"""
Script d'initialisation de la base de données avec données de démonstration
Exécutez: python init_db.py
"""

from app import app, db, User, Asset, Maintenance, Movement, Alert
from datetime import datetime, timedelta

def init_database():
    """Initialise la base de données avec des données de démonstration"""
    
    with app.app_context():
        # Supprimer les tables existantes
        db.drop_all()
        print("✓ Tables supprimées")
        
        # Créer les nouvelles tables
        db.create_all()
        print("✓ Tables créées")
        
        # ==================== CRÉER LES UTILISATEURS ====================
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@municipality.tn',
                'password': 'admin123',
                'full_name': 'Administrateur Système',
                'role': 'admin'
            },
            {
                'username': 'responsable',
                'email': 'responsable@municipality.tn',
                'password': 'pass123',
                'full_name': 'Mohamed Ben Ali',
                'role': 'responsable_patrimoine'
            },
            {
                'username': 'agent',
                'email': 'agent@municipality.tn',
                'password': 'pass123',
                'full_name': 'Ahmed Khaled',
                'role': 'agent_maintenance'
            },
            {
                'username': 'auditeur',
                'email': 'auditeur@municipality.tn',
                'password': 'pass123',
                'full_name': 'Fatima Zahra',
                'role': 'auditeur'
            },
            {
                'username': 'service_chief',
                'email': 'chief@municipality.tn',
                'password': 'pass123',
                'full_name': 'Omar Saïd',
                'role': 'responsable_service'
            }
        ]
        
        users = []
        user_qr_codes = ['USR001', 'USR002', 'USR003', 'USR004', 'USR005']
        for idx, user_data in enumerate(users_data):
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                qr_code=user_qr_codes[idx]  # Assigner un QR code unique
            )
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ {len(users)} utilisateurs créés")
        
        # ==================== CRÉER LES ACTIFS ====================
        assets_data = [
            # Bâtiments
            {
                'name': 'Mairie Centrale',
                'category': 'bâtiment',
                'description': 'Bâtiment administratif principal',
                'acquisition_date': datetime(2015, 3, 15).date(),
                'acquisition_value': 500000,
                'current_value': 450000,
                'location': 'Centre-ville, Rue de la Liberté',
                'status': 'actif',
                'assigned_to': 'Mohamed Ben Ali'
            },
            {
                'name': 'Centre de Santé',
                'category': 'bâtiment',
                'description': 'Centre médical municipal',
                'acquisition_date': datetime(2018, 6, 20).date(),
                'acquisition_value': 350000,
                'current_value': 320000,
                'location': 'Quartier Ouest',
                'status': 'actif',
                'assigned_to': 'Dr. Fatima'
            },
            {
                'name': 'Bibliothèque Municipale',
                'category': 'bâtiment',
                'description': 'Bibliothèque publique',
                'acquisition_date': datetime(2010, 1, 10).date(),
                'acquisition_value': 250000,
                'current_value': 180000,
                'location': 'Rue de la Culture',
                'status': 'actif',
                'assigned_to': 'Directeur Bibliothèque'
            },
            
            # Véhicules
            {
                'name': 'Ambulance 001',
                'category': 'véhicule',
                'description': 'Ambulance Mercedes Sprinter 2020',
                'acquisition_date': datetime(2020, 6, 15).date(),
                'acquisition_value': 85000,
                'current_value': 65000,
                'location': 'Centre de Santé',
                'status': 'actif',
                'assigned_to': 'Service de Santé'
            },
            {
                'name': 'Camion Poubelle 001',
                'category': 'véhicule',
                'description': 'Camion de collecte des déchets',
                'acquisition_date': datetime(2019, 4, 10).date(),
                'acquisition_value': 120000,
                'current_value': 90000,
                'location': 'Garage Municipal',
                'status': 'actif',
                'assigned_to': 'Service Propreté'
            },
            {
                'name': 'Véhicule de Service 001',
                'category': 'véhicule',
                'description': 'Peugeot 308 pour déplacements administratifs',
                'acquisition_date': datetime(2021, 2, 20).date(),
                'acquisition_value': 35000,
                'current_value': 28000,
                'location': 'Parking Mairie',
                'status': 'actif',
                'assigned_to': 'Direction'
            },
            
            # Équipements
            {
                'name': 'Serveur Informatique',
                'category': 'équipement',
                'description': 'Serveur Dell PowerEdge R750',
                'acquisition_date': datetime(2021, 9, 1).date(),
                'acquisition_value': 25000,
                'current_value': 18000,
                'location': 'Salle Informatique',
                'status': 'actif',
                'assigned_to': 'IT Manager'
            },
            {
                'name': 'Système de Climatisation',
                'category': 'équipement',
                'description': 'Climatisation centrale Mairie',
                'acquisition_date': datetime(2018, 5, 15).date(),
                'acquisition_value': 45000,
                'current_value': 35000,
                'location': 'Mairie Centrale',
                'status': 'actif',
                'assigned_to': 'Maintenance'
            },
            {
                'name': 'Groupe Électrogène',
                'category': 'équipement',
                'description': 'Générateur 50 kVA',
                'acquisition_date': datetime(2017, 11, 20).date(),
                'acquisition_value': 30000,
                'current_value': 20000,
                'location': 'Garage Municipal',
                'status': 'maintenance',
                'assigned_to': 'Service Technique'
            },
            
            # Mobilier
            {
                'name': 'Bureau Directeur',
                'category': 'mobilier',
                'description': 'Bureau exécutif en bois massif',
                'acquisition_date': datetime(2015, 8, 10).date(),
                'acquisition_value': 5000,
                'current_value': 3000,
                'location': 'Bureau Directeur',
                'status': 'actif',
                'assigned_to': 'Direction'
            },
            {
                'name': 'Chaises de Réunion (Lot)',
                'category': 'mobilier',
                'description': '20 chaises de réunion',
                'acquisition_date': datetime(2019, 3, 15).date(),
                'acquisition_value': 8000,
                'current_value': 5000,
                'location': 'Salle de Réunion',
                'status': 'actif',
                'assigned_to': 'Administration'
            },
            
            # Terrains
            {
                'name': 'Terrain Parc Municipal',
                'category': 'terrain',
                'description': 'Terrain pour parc public - 2 hectares',
                'acquisition_date': datetime(2010, 1, 1).date(),
                'acquisition_value': 200000,
                'current_value': 250000,
                'location': 'Quartier Nord',
                'status': 'actif',
                'assigned_to': 'Service Environnement'
            },
            {
                'name': 'Terrain Futur Stade',
                'category': 'terrain',
                'description': 'Terrain réservé pour construction stade',
                'acquisition_date': datetime(2018, 7, 5).date(),
                'acquisition_value': 150000,
                'current_value': 160000,
                'location': 'Quartier Est',
                'status': 'actif',
                'assigned_to': 'Service Urbanisme'
            }
        ]
        
        assets = []
        qr_codes = ['QR001', 'QR002', 'QR003', 'QR004', 'QR005', 'QR006', 'QR007', 'QR008', 'QR009', 'QR010', 'QR011', 'QR012', 'QR013']
        for idx, asset_data in enumerate(assets_data):
            asset = Asset(**asset_data)
            asset.qr_code = qr_codes[idx]  # Assigner un code QR
            assets.append(asset)
            db.session.add(asset)
        
        db.session.commit()
        print(f"✓ {len(assets)} actifs créés")
        
        # ==================== CRÉER LES MAINTENANCES ====================
        maintenances_data = [
            {
                'asset_id': 1,
                'maintenance_type': 'préventive',
                'scheduled_date': datetime.now().date() + timedelta(days=30),
                'description': 'Inspection générale et nettoyage',
                'cost': 5000,
                'status': 'planifiée'
            },
            {
                'asset_id': 4,
                'maintenance_type': 'préventive',
                'scheduled_date': datetime.now().date() + timedelta(days=15),
                'description': 'Révision moteur et changement d\'huile',
                'cost': 3500,
                'status': 'planifiée'
            },
            {
                'asset_id': 7,
                'maintenance_type': 'corrective',
                'scheduled_date': datetime.now().date() + timedelta(days=5),
                'description': 'Réparation climatisation',
                'cost': 2000,
                'status': 'en_cours'
            },
            {
                'asset_id': 2,
                'maintenance_type': 'préventive',
                'scheduled_date': datetime.now().date() - timedelta(days=10),
                'completed_date': datetime.now().date() - timedelta(days=5),
                'description': 'Maintenance annuelle',
                'cost': 4000,
                'status': 'complétée'
            },
            {
                'asset_id': 5,
                'maintenance_type': 'préventive',
                'scheduled_date': datetime.now().date() + timedelta(days=45),
                'description': 'Révision générale et entretien',
                'cost': 6000,
                'status': 'planifiée'
            }
        ]
        
        maintenances = []
        for maint_data in maintenances_data:
            maintenance = Maintenance(**maint_data)
            maintenances.append(maintenance)
            db.session.add(maintenance)
        
        db.session.commit()
        print(f"✓ {len(maintenances)} maintenances créées")
        
        # ==================== CRÉER LES MOUVEMENTS ====================
        movements_data = [
            {
                'asset_id': 4,
                'from_location': 'Garage Municipal',
                'to_location': 'Centre de Santé',
                'reason': 'Affectation au service de santé',
                'created_by': 'Mohamed Ben Ali'
            },
            {
                'asset_id': 5,
                'from_location': 'Parking Mairie',
                'to_location': 'Garage Municipal',
                'reason': 'Maintenance programmée',
                'created_by': 'Ahmed Khaled'
            }
        ]
        
        movements = []
        for move_data in movements_data:
            movement = Movement(**move_data)
            movements.append(movement)
            db.session.add(movement)
        
        db.session.commit()
        print(f"✓ {len(movements)} mouvements créés")
        
        # ==================== CRÉER LES ALERTES ====================
        alerts_data = [
            {
                'asset_id': 7,
                'alert_type': 'maintenance',
                'message': 'Maintenance corrective urgente requise',
                'due_date': datetime.now().date() + timedelta(days=5),
                'is_read': False
            },
            {
                'asset_id': 4,
                'alert_type': 'maintenance',
                'message': 'Maintenance préventive prévue dans 15 jours',
                'due_date': datetime.now().date() + timedelta(days=15),
                'is_read': False
            },
            {
                'asset_id': 3,
                'alert_type': 'amortissement',
        print(f"   • Utilisateurs: {len(users)}")
        print(f"   • Actifs: {len(assets)}")
        print(f"   • Maintenances: {len(maintenances)}")
        print(f"   • Mouvements: {len(movements)}")
        print(f"   • Alertes: {len(alerts)}")
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
