#!/usr/bin/env python3
"""
Script pour nettoyer les utilisateurs statiques et créer vos propres utilisateurs
"""

import sqlite3
import os
from datetime import datetime
import secrets
import string

def connect_db():
    """Connexion à la base de données"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'patrimoine.db')
    return sqlite3.connect(db_path)

def generate_qr_code():
    """Générer un code QR unique"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def clean_static_users():
    """Supprimer tous les utilisateurs statiques sauf admin"""
    print("🗑️ Suppression des utilisateurs statiques...")
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Garder seulement l'admin
        cursor.execute("DELETE FROM users WHERE username != 'admin'")
        deleted_count = cursor.rowcount
        
        # Nettoyer aussi les relations dans group_members
        cursor.execute("DELETE FROM group_members WHERE user_id NOT IN (SELECT id FROM users)")
        
        # Nettoyer les messages des utilisateurs supprimés
        cursor.execute("DELETE FROM messages WHERE sender_id NOT IN (SELECT id FROM users) OR recipient_id NOT IN (SELECT id FROM users)")
        
        conn.commit()
        print(f"✅ {deleted_count} utilisateurs statiques supprimés")
        
        # Vérifier l'admin restant
        cursor.execute("SELECT id, username, full_name FROM users")
        remaining = cursor.fetchall()
        print(f"👤 Utilisateurs restants: {len(remaining)}")
        for user in remaining:
            print(f"   - {user[1]} ({user[2]})")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_custom_users():
    """Créer vos utilisateurs personnalisés"""
    print("\n👥 Création de vos utilisateurs personnalisés...")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Vos utilisateurs personnalisés
    custom_users = [
        {
            'username': 'sahar',
            'email': 'sahargaiche6@gmail.com',
            'full_name': 'Sahar Ghribi',
            'role': 'admin',
            'password': 'sahar123'
        },
        {
            'username': 'samar',
            'email': 'samargaiche82@gmail.com', 
            'full_name': 'Samar Gaiche',
            'role': 'responsable_patrimoine',
            'password': 'samar123'
        },
        {
            'username': 'mohamed',
            'email': 'mohamed@patrimoine.tn',
            'full_name': 'Mohamed Ben Ali',
            'role': 'agent_maintenance',
            'password': 'mohamed123'
        },
        {
            'username': 'fatima',
            'email': 'fatima@patrimoine.tn',
            'full_name': 'Fatima Zahra',
            'role': 'auditeur',
            'password': 'fatima123'
        }
    ]
    
    try:
        from werkzeug.security import generate_password_hash
        
        for user_data in custom_users:
            # Générer un QR code unique
            qr_code = generate_qr_code()
            
            # Vérifier si l'utilisateur existe déjà
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_data['username'],))
            existing = cursor.fetchone()
            
            if existing:
                # Mettre à jour l'utilisateur existant
                cursor.execute("""
                    UPDATE users SET 
                    email = ?, full_name = ?, role = ?, 
                    password_hash = ?, qr_code = ?
                    WHERE username = ?
                """, (
                    user_data['email'],
                    user_data['full_name'], 
                    user_data['role'],
                    generate_password_hash(user_data['password']),
                    qr_code,
                    user_data['username']
                ))
                print(f"✅ Mis à jour: {user_data['username']} (QR: {qr_code})")
            else:
                # Créer un nouvel utilisateur
                cursor.execute("""
                    INSERT INTO users (username, email, full_name, role, password_hash, qr_code, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_data['username'],
                    user_data['email'],
                    user_data['full_name'],
                    user_data['role'],
                    generate_password_hash(user_data['password']),
                    qr_code,
                    datetime.utcnow().isoformat()
                ))
                print(f"✅ Créé: {user_data['username']} (QR: {qr_code})")
        
        conn.commit()
        print(f"\n🎉 {len(custom_users)} utilisateurs personnalisés créés/mis à jour!")
        
        # Afficher tous les utilisateurs avec leurs QR codes
        cursor.execute("SELECT username, full_name, email, role, qr_code FROM users ORDER BY id")
        all_users = cursor.fetchall()
        
        print("\n📋 Tous vos utilisateurs:")
        print("-" * 80)
        print(f"{'Username':<12} {'Nom Complet':<20} {'Email':<25} {'Rôle':<15} {'QR Code':<8}")
        print("-" * 80)
        for user in all_users:
            print(f"{user[0]:<12} {user[1]:<20} {user[2]:<25} {user[3]:<15} {user[4]:<8}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_qr_codes_file():
    """Créer un fichier avec tous les QR codes"""
    print("\n📱 Création du fichier QR codes...")
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username, full_name, qr_code FROM users ORDER BY username")
        users = cursor.fetchall()
        
        qr_content = "# 📱 VOS QR CODES UTILISATEURS\n\n"
        qr_content += f"**Généré le:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        qr_content += "## 🔍 Codes QR pour Scanner\n\n"
        
        for user in users:
            qr_content += f"### 👤 {user[1]} (@{user[0]})\n"
            qr_content += f"**QR Code:** `{user[2]}`\n"
            qr_content += f"**URL de scan:** `http://localhost:3000/qr-scanner?code={user[2]}`\n\n"
        
        qr_content += "## 📱 Comment Scanner\n\n"
        qr_content += "1. Allez sur: `http://localhost:3000/qr-scanner`\n"
        qr_content += "2. Entrez le code QR manuellement\n"
        qr_content += "3. Ou scannez avec votre caméra\n\n"
        qr_content += "## 🔗 Liens Directs\n\n"
        
        for user in users:
            qr_content += f"- [{user[1]}](http://localhost:3000/qr-scanner?code={user[2]})\n"
        
        # Sauvegarder le fichier
        qr_file_path = os.path.join(os.path.dirname(__file__), '..', 'QR_CODES_UTILISATEURS.md')
        with open(qr_file_path, 'w', encoding='utf-8') as f:
            f.write(qr_content)
        
        print(f"✅ Fichier QR créé: {qr_file_path}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        conn.close()

def main():
    """Fonction principale"""
    print("🚀 NETTOYAGE ET CRÉATION D'UTILISATEURS PERSONNALISÉS")
    print("=" * 60)
    
    # Étape 1: Supprimer les utilisateurs statiques
    clean_static_users()
    
    # Étape 2: Créer vos utilisateurs
    create_custom_users()
    
    # Étape 3: Créer le fichier QR codes
    create_qr_codes_file()
    
    print("\n" + "=" * 60)
    print("✅ TERMINÉ! Vos utilisateurs personnalisés sont prêts!")
    print("\n📋 Prochaines étapes:")
    print("1. Connectez-vous avec: sahar / sahar123")
    print("2. Testez le scanner QR: http://localhost:3000/qr-scanner")
    print("3. Consultez le fichier: QR_CODES_UTILISATEURS.md")

if __name__ == "__main__":
    main()
