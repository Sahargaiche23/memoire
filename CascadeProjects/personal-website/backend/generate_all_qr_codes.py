#!/usr/bin/env python3
"""
Script pour générer/régénérer les QR codes de tous les utilisateurs
"""

import os
import sys
import random
import string
import qrcode
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, User

QR_CODES_FOLDER = os.path.join(os.path.dirname(__file__), 'qr_codes')
Path(QR_CODES_FOLDER).mkdir(exist_ok=True)

def generate_unique_qr_code():
    """Génère un code QR unique de 8 caractères"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_qr_code_image(username, qr_code, full_name=''):
    """Crée l'image QR code pour un utilisateur"""
    try:
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(qr_code)
        qr.make(fit=True)
        
        # Créer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder l'image
        filename = f"qr_{username}_{qr_code}.png"
        filepath = os.path.join(QR_CODES_FOLDER, filename)
        img.save(filepath)
        
        print(f"✅ QR Code créé: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Erreur création QR code: {e}")
        return None

def main():
    """Générer les QR codes pour tous les utilisateurs"""
    
    with app.app_context():
        users = User.query.all()
        
        print(f"\n🎫 Génération des QR codes pour {len(users)} utilisateurs...\n")
        
        updated = 0
        created = 0
        errors = 0
        
        for user in users:
            try:
                # Si l'utilisateur n'a pas de QR code, en créer un
                if not user.qr_code:
                    user.qr_code = generate_unique_qr_code()
                    db.session.add(user)
                    created += 1
                    print(f"🆕 Nouveau QR code pour {user.username}: {user.qr_code}")
                else:
                    print(f"📋 QR code existant pour {user.username}: {user.qr_code}")
                
                # Créer/recréer l'image QR code
                qr_filename = create_qr_code_image(
                    username=user.username,
                    qr_code=user.qr_code,
                    full_name=user.full_name or ''
                )
                
                if qr_filename:
                    updated += 1
                else:
                    errors += 1
                    
            except Exception as e:
                print(f"❌ Erreur pour {user.username}: {e}")
                errors += 1
        
        # Sauvegarder les changements
        try:
            db.session.commit()
            print(f"\n✅ Base de données mise à jour!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors de la sauvegarde: {e}")
        
        # Résumé
        print(f"\n" + "="*50)
        print(f"📊 RÉSUMÉ:")
        print(f"   - Utilisateurs traités: {len(users)}")
        print(f"   - QR codes créés: {created}")
        print(f"   - Images générées: {updated}")
        print(f"   - Erreurs: {errors}")
        print(f"="*50 + "\n")
        
        # Lister les QR codes générés
        print("📁 Fichiers QR codes créés:")
        qr_files = sorted(os.listdir(QR_CODES_FOLDER))
        for f in qr_files:
            if f.endswith('.png'):
                filepath = os.path.join(QR_CODES_FOLDER, f)
                size = os.path.getsize(filepath)
                print(f"   ✓ {f} ({size} bytes)")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎫 GÉNÉRATEUR DE QR CODES")
    print("="*50 + "\n")
    main()
    print("\n✨ Terminé!\n")
