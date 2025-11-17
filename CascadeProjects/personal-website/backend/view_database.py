#!/usr/bin/env python3
"""
Script pour visualiser le contenu de la base de données
Usage: python3 view_database.py
"""

import sqlite3
import os
from datetime import datetime

def connect_db():
    """Connexion à la base de données"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'patrimoine.db')
    return sqlite3.connect(db_path)

def print_table_header(title):
    """Afficher un en-tête de table"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")

def view_users():
    """Afficher tous les utilisateurs"""
    print_table_header("UTILISATEURS")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, full_name, email, role, created_at FROM users ORDER BY id")
    users = cursor.fetchall()
    
    print(f"{'ID':<3} {'Username':<15} {'Nom Complet':<20} {'Email':<25} {'Rôle':<20} {'Créé le':<12}")
    print("-" * 100)
    
    for user in users:
        created_date = user[5][:10] if user[5] else 'N/A'
        print(f"{user[0]:<3} {user[1]:<15} {user[2]:<20} {user[3]:<25} {user[4]:<20} {created_date:<12}")
    
    print(f"\n📈 Total: {len(users)} utilisateurs")
    conn.close()

def view_assets():
    """Afficher tous les actifs"""
    print_table_header("ACTIFS")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, category, status, current_value, location FROM assets ORDER BY category, id")
    assets = cursor.fetchall()
    
    print(f"{'ID':<3} {'Nom':<20} {'Catégorie':<12} {'Statut':<12} {'Valeur':<10} {'Localisation':<15}")
    print("-" * 80)
    
    for asset in assets:
        value = f"{asset[4]:.0f}€" if asset[4] else 'N/A'
        location = asset[5] if asset[5] else 'N/A'
        print(f"{asset[0]:<3} {asset[1]:<20} {asset[2]:<12} {asset[3]:<12} {value:<10} {location:<15}")
    
    print(f"\n📈 Total: {len(assets)} actifs")
    conn.close()

def view_maintenances():
    """Afficher toutes les maintenances"""
    print_table_header("MAINTENANCES")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.id, a.name, m.maintenance_type, m.scheduled_date, m.status, m.description 
        FROM maintenances m 
        LEFT JOIN assets a ON m.asset_id = a.id 
        ORDER BY m.scheduled_date DESC
    """)
    maintenances = cursor.fetchall()
    
    print(f"{'ID':<3} {'Actif':<20} {'Type':<12} {'Date Prévue':<12} {'Statut':<12} {'Description':<30}")
    print("-" * 95)
    
    for maintenance in maintenances:
        scheduled = maintenance[3] if maintenance[3] else 'N/A'
        description = maintenance[5][:30] if maintenance[5] else 'N/A'
        asset_name = maintenance[1] if maintenance[1] else 'N/A'
        mtype = maintenance[2] if maintenance[2] else 'N/A'
        status = maintenance[4] if maintenance[4] else 'N/A'
        print(f"{maintenance[0]:<3} {asset_name:<20} {mtype:<12} {scheduled:<12} {status:<12} {description:<30}")
    
    print(f"\n📈 Total: {len(maintenances)} maintenances")
    conn.close()

def view_groups():
    """Afficher tous les groupes"""
    print_table_header("GROUPES")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Compter les membres de chaque groupe
    cursor.execute("""
        SELECT g.id, g.name, g.description, COUNT(gm.user_id) as member_count
        FROM groups g
        LEFT JOIN group_members gm ON g.id = gm.group_id
        GROUP BY g.id, g.name, g.description
        ORDER BY g.id
    """)
    groups = cursor.fetchall()
    
    print(f"{'ID':<3} {'Nom':<20} {'Description':<40} {'Membres':<8}")
    print("-" * 75)
    
    for group in groups:
        description = group[2][:40] if group[2] else 'N/A'
        print(f"{group[0]:<3} {group[1]:<20} {description:<40} {group[3]:<8}")
    
    print(f"\n📈 Total: {len(groups)} groupes")
    conn.close()

def view_messages():
    """Afficher les messages récents"""
    print_table_header("MESSAGES RÉCENTS")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.id, u1.full_name as sender, u2.full_name as recipient, 
               m.subject, m.content, m.created_at, m.is_read
        FROM messages m
        LEFT JOIN users u1 ON m.sender_id = u1.id
        LEFT JOIN users u2 ON m.recipient_id = u2.id
        ORDER BY m.created_at DESC
        LIMIT 10
    """)
    messages = cursor.fetchall()
    
    print(f"{'ID':<3} {'Expéditeur':<15} {'Destinataire':<15} {'Sujet':<15} {'Contenu':<25} {'Date':<12} {'Lu':<3}")
    print("-" * 95)
    
    for message in messages:
        content = message[4][:25] if message[4] else 'N/A'
        created_date = message[5][:10] if message[5] else 'N/A'
        is_read = '✅' if message[6] else '❌'
        print(f"{message[0]:<3} {message[1]:<15} {message[2]:<15} {message[3]:<15} {content:<25} {created_date:<12} {is_read:<3}")
    
    print(f"\n📈 Total affiché: {len(messages)} messages (10 plus récents)")
    conn.close()

def view_statistics():
    """Afficher les statistiques générales"""
    print_table_header("STATISTIQUES GÉNÉRALES")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Compter les éléments
    tables = ['users', 'assets', 'maintenances', 'groups', 'messages']
    stats = {}
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        stats[table] = count
    
    # Statistiques par catégorie d'actifs
    cursor.execute("SELECT category, COUNT(*) FROM assets GROUP BY category")
    asset_categories = cursor.fetchall()
    
    # Statistiques par rôle d'utilisateur
    cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    user_roles = cursor.fetchall()
    
    print("📊 Nombre total d'éléments:")
    print("-" * 30)
    for table, count in stats.items():
        table_name = {
            'users': 'Utilisateurs',
            'assets': 'Actifs', 
            'maintenances': 'Maintenances',
            'groups': 'Groupes',
            'messages': 'Messages'
        }[table]
        print(f"{table_name:<15}: {count:>5}")
    
    print("\n📊 Actifs par catégorie:")
    print("-" * 30)
    for category, count in asset_categories:
        print(f"{category.capitalize():<15}: {count:>5}")
    
    print("\n📊 Utilisateurs par rôle:")
    print("-" * 30)
    for role, count in user_roles:
        print(f"{role:<15}: {count:>5}")
    
    conn.close()

def main():
    """Fonction principale"""
    print("🗄️  VISUALISEUR DE BASE DE DONNÉES - PATRIMOINE MUNICIPAL")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Vérifier que la base de données existe
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'patrimoine.db')
        if not os.path.exists(db_path):
            print(f"❌ Base de données non trouvée: {db_path}")
            return
        
        print(f"📍 Base de données: {db_path}")
        
        # Afficher toutes les données
        view_statistics()
        view_users()
        view_assets()
        view_maintenances()
        view_groups()
        view_messages()
        
        print(f"\n{'='*70}")
        print("✅ Visualisation terminée avec succès!")
        print("💡 Pour une vue interactive, utilisez: sqlite3 instance/patrimoine.db")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
