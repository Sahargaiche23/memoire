"""
Script de migration pour transformer les alertes dynamiques en alertes stockées en BDD
"""

from app import app, db, Alert
from datetime import datetime

def migrate_alerts_table():
    """
    Créer/mettre à jour la table alerts avec la nouvelle structure
    """
    with app.app_context():
        print("🔄 Début de la migration de la table alerts...")
        
        try:
            # Supprimer l'ancienne table si elle existe
            Alert.__table__.drop(db.engine, checkfirst=True)
            print("✅ Ancienne table alerts supprimée")
        except Exception as e:
            print(f"ℹ️ Pas d'ancienne table à supprimer: {e}")
        
        try:
            # Créer la nouvelle table avec la structure améliorée
            Alert.__table__.create(db.engine, checkfirst=True)
            print("✅ Nouvelle table alerts créée avec succès!")
            
            # Afficher la structure de la table
            print("\n📊 Structure de la nouvelle table Alert:")
            print("  - id (Integer, Primary Key)")
            print("  - asset_id (Integer, Foreign Key)")
            print("  - maintenance_id (Integer, Foreign Key)")
            print("  - alert_type (String) - MAINTENANCE_URGENT | MAINTENANCE_LATE | ASSET_MAINTENANCE_REQUIRED")
            print("  - priority (String) - HIGH | CRITICAL | MEDIUM")
            print("  - message (Text)")
            print("  - due_date (Date)")
            print("  - days_count (Integer)")
            print("  - is_read (Boolean)")
            print("  - is_active (Boolean)")
            print("  - is_dismissed (Boolean) - Ignorée définitivement par l'utilisateur")
            print("  - created_at (DateTime)")
            print("  - updated_at (DateTime)")
            
            print("\n✅ Migration terminée avec succès!")
            print("\n💡 Prochaine étape: Redémarrez le backend pour générer les premières alertes")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la table: {e}")
            raise e

if __name__ == '__main__':
    migrate_alerts_table()
