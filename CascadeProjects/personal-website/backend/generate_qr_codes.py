#!/usr/bin/env python3
"""
Générateur de QR codes visuels pour les utilisateurs
Crée des QR codes comme dans l'image avec "Scan ME!"
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import sqlite3
from datetime import datetime

def connect_db():
    """Connexion à la base de données"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'patrimoine.db')
    return sqlite3.connect(db_path)

def create_qr_code_with_design(data, filename, user_name="Utilisateur"):
    """Créer un QR code avec design comme l'image"""
    
    # Créer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Créer l'image QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Créer une image plus grande pour le design
    width, height = 800, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Dessiner le fond avec dégradé (simulé avec des rectangles)
    for i in range(height):
        color_intensity = int(240 - (i * 40 / height))
        color = (color_intensity, color_intensity, 255)
        draw.line([(0, i), (width, i)], fill=color)
    
    # Dessiner le smartphone (rectangle arrondi)
    phone_x, phone_y = 50, 100
    phone_width, phone_height = 300, 450
    
    # Corps du téléphone
    draw.rounded_rectangle(
        [phone_x, phone_y, phone_x + phone_width, phone_y + phone_height],
        radius=30,
        fill='black'
    )
    
    # Écran du téléphone
    screen_margin = 20
    draw.rounded_rectangle(
        [phone_x + screen_margin, phone_y + screen_margin, 
         phone_x + phone_width - screen_margin, phone_y + phone_height - screen_margin],
        radius=20,
        fill='white'
    )
    
    # Barre de statut du téléphone
    draw.rectangle(
        [phone_x + screen_margin + 10, phone_y + screen_margin + 10,
         phone_x + phone_width - screen_margin - 10, phone_y + screen_margin + 20],
        fill='black'
    )
    
    # Redimensionner et placer le QR code dans l'écran
    qr_size = 200
    qr_img_resized = qr_img.resize((qr_size, qr_size))
    qr_x = phone_x + (phone_width - qr_size) // 2
    qr_y = phone_y + 150
    img.paste(qr_img_resized, (qr_x, qr_y))
    
    # Ajouter le texte "Scan ME!"
    try:
        # Essayer d'utiliser une police système
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        # Police par défaut si pas trouvée
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Texte "Scan"
    scan_text = "Scan"
    text_x = phone_x + phone_width + 50
    text_y = phone_y + 50
    draw.text((text_x, text_y), scan_text, fill='black', font=font_large)
    
    # Texte "ME!"
    me_text = "ME!"
    draw.text((text_x, text_y + 90), me_text, fill='black', font=font_large)
    
    # Nom de l'utilisateur
    draw.text((text_x, text_y + 200), user_name, fill='black', font=font_medium)
    
    # Code QR en texte
    draw.text((text_x, text_y + 260), f"Code: {data}", fill='gray', font=font_small)
    
    # URL de scan
    scan_url = f"http://localhost:3000/qr-scanner?code={data}"
    draw.text((text_x, text_y + 300), "Scanner sur:", fill='gray', font=font_small)
    draw.text((text_x, text_y + 330), "localhost:3000/qr-scanner", fill='blue', font=font_small)
    
    # Sauvegarder l'image
    img.save(filename, 'PNG', quality=95)
    print(f"✅ QR code créé: {filename}")

def generate_all_user_qr_codes():
    """Générer les QR codes pour tous les utilisateurs"""
    print("🎨 GÉNÉRATION DES QR CODES VISUELS")
    print("=" * 50)
    
    # Créer le dossier pour les QR codes
    qr_folder = os.path.join(os.path.dirname(__file__), '..', 'qr_codes')
    os.makedirs(qr_folder, exist_ok=True)
    
    # Récupérer tous les utilisateurs
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username, full_name, qr_code, email FROM users WHERE qr_code IS NOT NULL ORDER BY username")
        users = cursor.fetchall()
        
        print(f"📱 Génération de {len(users)} QR codes...")
        
        for user in users:
            username, full_name, qr_code, email = user
            
            # Nom du fichier
            filename = os.path.join(qr_folder, f"qr_{username}_{qr_code}.png")
            
            # Créer le QR code avec design
            create_qr_code_with_design(
                data=qr_code,
                filename=filename,
                user_name=full_name or username
            )
        
        print(f"\n🎉 {len(users)} QR codes générés dans: {qr_folder}")
        
        # Créer un fichier HTML pour visualiser tous les QR codes
        create_qr_gallery_html(users, qr_folder)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        conn.close()

def create_qr_gallery_html(users, qr_folder):
    """Créer une galerie HTML pour visualiser tous les QR codes"""
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 Galerie QR Codes - Patrimoine Municipal</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        h1 {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .subtitle {{
            text-align: center;
            color: #6c757d;
            margin-bottom: 40px;
            font-size: 1.2em;
        }}
        
        .qr-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}
        
        .qr-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .qr-card:hover {{
            transform: translateY(-5px);
        }}
        
        .qr-image {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            margin-bottom: 15px;
        }}
        
        .user-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .user-code {{
            color: #6c757d;
            font-family: 'Courier New', monospace;
            background: white;
            padding: 5px 10px;
            border-radius: 5px;
            display: inline-block;
            margin-bottom: 10px;
        }}
        
        .scan-link {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.3s ease;
        }}
        
        .scan-link:hover {{
            transform: scale(1.05);
        }}
        
        .stats {{
            background: #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        @media (max-width: 768px) {{
            .qr-grid {{
                grid-template-columns: 1fr;
            }}
            
            .container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Galerie QR Codes</h1>
        <p class="subtitle">Système de Gestion du Patrimoine Municipal</p>
        
        <div class="stats">
            <div class="stat-number">{len(users)}</div>
            <div>QR Codes Générés</div>
            <div style="margin-top: 10px; color: #6c757d;">
                Générés le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
            </div>
        </div>
        
        <div class="qr-grid">
"""
    
    for user in users:
        username, full_name, qr_code, email = user
        qr_filename = f"qr_{username}_{qr_code}.png"
        
        html_content += f"""
            <div class="qr-card">
                <img src="qr_codes/{qr_filename}" alt="QR Code {full_name}" class="qr-image">
                <div class="user-name">{full_name or username}</div>
                <div class="user-code">{qr_code}</div>
                <a href="http://localhost:3000/qr-scanner?code={qr_code}" class="scan-link" target="_blank">
                    📱 Scanner Maintenant
                </a>
            </div>
        """
    
    html_content += """
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 2px solid #e9ecef;">
            <p style="color: #6c757d;">
                💡 <strong>Comment utiliser:</strong> Cliquez sur "📱 Scanner Maintenant" ou allez sur 
                <a href="http://localhost:3000/qr-scanner" target="_blank">localhost:3000/qr-scanner</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    # Sauvegarder le fichier HTML
    html_file = os.path.join(os.path.dirname(qr_folder), 'qr_gallery.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"🌐 Galerie HTML créée: {html_file}")
    print(f"🔗 Ouvrez dans votre navigateur: file://{html_file}")

def main():
    """Fonction principale"""
    print("🎨 GÉNÉRATEUR DE QR CODES VISUELS")
    print("=" * 50)
    print("Création de QR codes comme dans l'image avec 'Scan ME!'")
    print()
    
    try:
        generate_all_user_qr_codes()
        
        print("\n" + "=" * 50)
        print("✅ GÉNÉRATION TERMINÉE!")
        print("\n📋 Fichiers créés:")
        print("   📁 qr_codes/ - Dossier avec tous les QR codes")
        print("   🌐 qr_gallery.html - Galerie pour visualiser")
        print("\n🚀 Prochaines étapes:")
        print("   1. Ouvrez qr_gallery.html dans votre navigateur")
        print("   2. Imprimez ou partagez vos QR codes")
        print("   3. Testez le scan sur: http://localhost:3000/qr-scanner")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
