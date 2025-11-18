#!/usr/bin/env python3
"""
Script pour créer des maintenances de test qui généreront des alertes dynamiques
"""

from app import app, db, Asset, Maintenance, User
from datetime import datetime, timedelta, date

def create_test_maintenances():
    """Créer des maintenances de test pour générer des alertes"""
    
    with app.app_context():
        print("🔧 Création de maintenances de test...\n")
        
        # Récupérer des actifs existants
        assets = Asset.query.all()
        if not assets:
            print("❌ Aucun actif trouvé. Créez des actifs d'abord.")
            return
        
        # Récupérer un utilisateur pour créer les maintenances
        user = User.query.first()
        if not user:
            print("❌ Aucun utilisateur trouvé.")
            return
        
        # Nettoyer les anciennes maintenances de test
        Maintenance.query.filter(Maintenance.description.like('%TEST%')).delete()
        db.session.commit()
        print("🗑️  Anciennes maintenances de test supprimées\n")
        
        maintenances_created = []
        
        # 1. MAINTENANCE EN RETARD (2 jours)
        if len(assets) >= 1:
            m1 = Maintenance(
                asset_id=assets[0].id,
                maintenance_type='corrective',
                description='TEST - Maintenance en retard de 2 jours',
                scheduled_date=date.today() - timedelta(days=2),
                status='planifié'
            )
            db.session.add(m1)
            maintenances_created.append(f"🔴 EN RETARD: {assets[0].name} (2 jours)")
        
        # 2. MAINTENANCE EN RETARD (5 jours)
        if len(assets) >= 2:
            m2 = Maintenance(
                asset_id=assets[1].id,
                maintenance_type='preventive',
                description='TEST - Maintenance en retard de 5 jours',
                scheduled_date=date.today() - timedelta(days=5),
                status='planifié'
            )
            db.session.add(m2)
            maintenances_created.append(f"🔴 EN RETARD: {assets[1].name} (5 jours)")
        
        # 3. MAINTENANCE URGENTE (dans 2 jours)
        if len(assets) >= 3:
            m3 = Maintenance(
                asset_id=assets[2].id,
                maintenance_type='preventive',
                description='TEST - Maintenance urgente dans 2 jours',
                scheduled_date=date.today() + timedelta(days=2),
                status='planifié'
            )
            db.session.add(m3)
            maintenances_created.append(f"🟡 URGENTE: {assets[2].name} (dans 2 jours)")
        
        # 4. MAINTENANCE URGENTE (dans 5 jours)
        if len(assets) >= 4:
            m4 = Maintenance(
                asset_id=assets[3].id,
                maintenance_type='corrective',
                description='TEST - Maintenance urgente dans 5 jours',
                scheduled_date=date.today() + timedelta(days=5),
                status='planifié'
            )
            db.session.add(m4)
            maintenances_created.append(f"🟡 URGENTE: {assets[3].name} (dans 5 jours)")
        
        # 5. MAINTENANCE NORMALE (dans 10 jours - ne génère PAS d'alerte)
        if len(assets) >= 5:
            m5 = Maintenance(
                asset_id=assets[4].id,
                maintenance_type='preventive',
                description='TEST - Maintenance normale dans 10 jours',
                scheduled_date=date.today() + timedelta(days=10),
                status='planifié'
            )
            db.session.add(m5)
            maintenances_created.append(f"⚪ NORMALE: {assets[4].name} (dans 10 jours - pas d'alerte)")
        
        # 6. Marquer un actif comme nécessitant maintenance
        if len(assets) >= 6:
            assets[5].status = 'maintenance_required'
            maintenances_created.append(f"🔧 ACTIF: {assets[5].name} nécessite maintenance")
        
        db.session.commit()
        
        print("✅ Maintenances de test créées avec succès!\n")
        print("📋 Résumé des maintenances:\n")
        for i, m in enumerate(maintenances_created, 1):
            print(f"  {i}. {m}")
        
        print("\n" + "="*60)
        print("🎯 ALERTES ATTENDUES SUR LE DASHBOARD:")
        print("="*60)
        
        # Compter les alertes attendues
        retard = sum(1 for m in maintenances_created if "EN RETARD" in m)
        urgente = sum(1 for m in maintenances_created if "URGENTE" in m)
        actif = sum(1 for m in maintenances_created if "ACTIF" in m)
        total = retard + urgente + actif
        
        print(f"\n  🔴 Maintenances en retard: {retard}")
        print(f"  🟡 Maintenances urgentes (≤7j): {urgente}")
        print(f"  🔧 Actifs nécessitant maintenance: {actif}")
        print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"  📊 TOTAL ALERTES: {total}\n")
        
        print("🔄 Allez sur le Dashboard et cliquez sur le bouton 🔄 pour actualiser!")
        print()

if __name__ == '__main__':
    create_test_maintenances()
