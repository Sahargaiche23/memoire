#!/usr/bin/env python3
"""
Script pour générer les images UML à partir des fichiers PlantUML
Utilise le serveur PlantUML en ligne ou l'installation locale
"""

import subprocess
import os
import sys
import zlib
import base64
import string
import requests

def plantuml_encode(plantuml_text):
    """Encode le texte PlantUML pour l'URL du serveur"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    
    plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    
    b64 = base64.b64encode(compressed_string).decode('utf-8')
    
    # Conversion base64 vers plantuml encoding
    result = []
    for char in b64:
        if char in base64_alphabet:
            result.append(plantuml_alphabet[base64_alphabet.index(char)])
        elif char == '=':
            break
    
    return ''.join(result)

def generate_with_server(puml_file, output_file):
    """Génère l'image via le serveur PlantUML en ligne"""
    print(f"📡 Génération via serveur en ligne: {puml_file}")
    
    with open(puml_file, 'r', encoding='utf-8') as f:
        plantuml_code = f.read()
    
    encoded = plantuml_encode(plantuml_code)
    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    
    print(f"🌐 URL: {url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"✅ Image générée: {output_file}")
        return True
    else:
        print(f"❌ Erreur serveur: {response.status_code}")
        return False

def generate_with_local(puml_file, output_file):
    """Génère l'image avec PlantUML local"""
    print(f"🖥️  Génération locale: {puml_file}")
    
    try:
        result = subprocess.run(
            ['plantuml', '-tpng', puml_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # PlantUML génère automatiquement le .png
            expected_output = puml_file.replace('.puml', '.png')
            if os.path.exists(expected_output):
                if expected_output != output_file:
                    os.rename(expected_output, output_file)
                print(f"✅ Image générée: {output_file}")
                return True
        else:
            print(f"❌ Erreur: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ PlantUML non installé")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Liste des fichiers à générer
    files_to_generate = [
        ('use_case_global.puml', 'use_case_global.png'),
    ]
    
    print("\n🎨 GÉNÉRATION DES DIAGRAMMES UML")
    print("=" * 60)
    
    # Essayer d'abord avec PlantUML local
    plantuml_available = subprocess.run(
        ['which', 'plantuml'],
        capture_output=True
    ).returncode == 0
    
    if plantuml_available:
        print("✅ PlantUML local détecté\n")
        method = 'local'
    else:
        print("⚠️  PlantUML local non disponible")
        print("📡 Utilisation du serveur en ligne\n")
        method = 'server'
    
    success_count = 0
    for puml_file, output_file in files_to_generate:
        puml_path = os.path.join(script_dir, puml_file)
        output_path = os.path.join(script_dir, output_file)
        
        if not os.path.exists(puml_path):
            print(f"⚠️  Fichier non trouvé: {puml_file}")
            continue
        
        print(f"\n📄 Traitement: {puml_file}")
        print("-" * 60)
        
        if method == 'local':
            success = generate_with_local(puml_path, output_path)
        else:
            success = generate_with_server(puml_path, output_path)
        
        if success:
            success_count += 1
            # Afficher la taille du fichier
            size = os.path.getsize(output_path)
            print(f"📊 Taille: {size:,} bytes")
    
    print("\n" + "=" * 60)
    print(f"✅ {success_count}/{len(files_to_generate)} diagrammes générés avec succès")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
