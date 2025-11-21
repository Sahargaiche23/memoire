#!/usr/bin/env python3
"""
Script de test pour générer et afficher les alertes
"""

from app import app, db, generate_and_update_alerts, Alert, Maintenance, Asset
from datetime import datetime, date, timedelta

def test_alerts():
    with app.app_context():
        print("\n" + "="*60)
        print("🧪 TEST SYSTÈME D'ALERTES")
        print("="*60 + "\n")
        
        # 1. Afficher les maintenances planifiées
        print("📋 MAINTENANCES PLANIFIÉES:")
        print("-" * 60)
        maintenances = Maintenance.query.filter_by(status='planifié').all()
        
        if not maintenances:
            print("⚠️ Aucune maintenance planifiée trouvée!")
            print("\n💡 Pour tester:")
            print("   1. Allez sur http://localhost:3000/maintenance")
            print("   2. Créez une maintenance avec date < 7 jours")
            print("   3. Relancez ce script\n")
        else:
            today = date.today()
            for m in maintenances:
                asset = db.session.get(Asset, m.asset_id) if m.asset_id else None
                days_diff = (m.scheduled_date - today).days
                
                status_emoji = "🚨" if days_diff < 0 else ("⚠️" if days_diff <= 7 else "✅")
                
                print(f"{status_emoji} ID: {m.id}")
                print(f"   Actif: {asset.name if asset else 'N/A'}")
                print(f"   Date prévue: {m.scheduled_date}")
                print(f"   Jours: {days_diff}")
                print(f"   Type: {m.maintenance_type}")
                print()
        
        # 2. Générer les alertes
        print("\n🔄 GÉNÉRATION DES ALERTES...")
        print("-" * 60)
        try:
            alerts_created, alerts_updated = generate_and_update_alerts()
            print(f"✅ Alertes créées: {alerts_created}")
            print(f"✅ Alertes mises à jour: {alerts_updated}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return
        
        # 3. Afficher les alertes générées
        print("\n🔔 ALERTES ACTIVES:")
        print("-" * 60)
        alerts = Alert.query.filter_by(is_active=True).order_by(Alert.priority.desc()).all()
        
        if not alerts:
            print("ℹ️ Aucune alerte active")
        else:
            priority_emoji = {
                'CRITICAL': '🚨',
                'HIGH': '⚠️',
                'MEDIUM': '🔧'
            }
            
            for alert in alerts:
                emoji = priority_emoji.get(alert.priority, '📢')
                print(f"\n{emoji} ALERTE #{alert.id}")
                print(f"   Type: {alert.alert_type}")
                print(f"   Priorité: {alert.priority}")
                print(f"   Message: {alert.message}")
                if alert.days_count:
                    print(f"   Jours: {alert.days_count}")
                print(f"   Lue: {'Oui' if alert.is_read else 'Non'}")
                print(f"   Créée: {alert.created_at.strftime('%d/%m/%Y %H:%M')}")
        
        # 4. Statistiques
        print("\n📊 STATISTIQUES:")
        print("-" * 60)
        total_alerts = Alert.query.filter_by(is_active=True).count()
        unread_alerts = Alert.query.filter_by(is_active=True, is_read=False).count()
        critical_alerts = Alert.query.filter_by(is_active=True, priority='CRITICAL').count()
        high_alerts = Alert.query.filter_by(is_active=True, priority='HIGH').count()
        
        print(f"Total alertes: {total_alerts}")
        print(f"Non lues: {unread_alerts}")
        print(f"Critiques: {critical_alerts}")
        print(f"Hautes: {high_alerts}")
        
        print("\n" + "="*60)
        print("✅ TEST TERMINÉ!")
        print("="*60 + "\n")
        
        print("💡 PROCHAINES ÉTAPES:")
        print("   1. Ouvrez http://localhost:3000")
        print("   2. Allez sur Dashboard")
        print("   3. Vérifiez les alertes affichées")
        print("   4. Cliquez sur une alerte pour la marquer comme lue\n")

if __name__ == '__main__':
    test_alerts()
