#!/usr/bin/env python3
"""
Génère l'image PNG du diagramme de cas d'utilisation via serveur PlantUML
"""
import requests
import os

def generate_png_from_server(puml_file, output_png):
    """Génère PNG via le serveur PlantUML officiel"""
    print(f"\n🎨 Génération de l'image: {puml_file}")
    print("=" * 60)
    
    # Lire le fichier PlantUML
    with open(puml_file, 'r', encoding='utf-8') as f:
        plantuml_code = f.read()
    
    # Envoyer au serveur PlantUML (méthode POST)
    url = "http://www.plantuml.com/plantuml/png/"
    
    try:
        response = requests.post(
            url,
            data={'text': plantuml_code},
            timeout=30
        )
        
        if response.status_code == 200:
            # Sauvegarder l'image
            with open(output_png, 'wb') as f:
                f.write(response.content)
            
            size = os.path.getsize(output_png)
            print(f"✅ Image générée avec succès!")
            print(f"📊 Fichier: {output_png}")
            print(f"📦 Taille: {size:,} bytes ({size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ Erreur serveur: {response.status_code}")
            
            # Essayer méthode alternative
            print("\n🔄 Essai méthode alternative...")
            return generate_png_alternative(plantuml_code, output_png)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\n🔄 Essai méthode alternative...")
        return generate_png_alternative(plantuml_code, output_png)

def generate_png_alternative(plantuml_code, output_png):
    """Méthode alternative via proxy"""
    import zlib
    import base64
    
    # Compression PlantUML
    compressed = zlib.compress(plantuml_code.encode('utf-8'))[2:-4]
    encoded = base64.b64encode(compressed).decode('utf-8')
    
    # Conversion base64 -> PlantUML encoding
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    base64_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    
    result = []
    for char in encoded:
        if char in base64_alphabet:
            idx = base64_alphabet.index(char)
            if idx < len(plantuml_alphabet):
                result.append(plantuml_alphabet[idx])
        elif char == '=':
            break
    
    plantuml_encoded = ''.join(result)
    
    # URL alternative
    url = f"https://kroki.io/plantuml/png/{plantuml_encoded}"
    
    try:
        print(f"🌐 URL alternative: {url[:80]}...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            with open(output_png, 'wb') as f:
                f.write(response.content)
            
            size = os.path.getsize(output_png)
            print(f"✅ Image générée via serveur alternatif!")
            print(f"📊 Fichier: {output_png}")
            print(f"📦 Taille: {size:,} bytes ({size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ Erreur serveur alternatif: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur méthode alternative: {e}")
        return False

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    puml_file = os.path.join(script_dir, 'use_case_simple.puml')
    output_png = os.path.join(script_dir, 'use_case_diagram.png')
    
    if not os.path.exists(puml_file):
        print(f"❌ Fichier non trouvé: {puml_file}")
        exit(1)
    
    success = generate_png_from_server(puml_file, output_png)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 DIAGRAMME GÉNÉRÉ AVEC SUCCÈS!")
        print("=" * 60)
        print(f"\n📍 Emplacement: {output_png}")
        print("\n💡 Ouvrir l'image:")
        print(f"   xdg-open {output_png}")
        print(f"   ou double-cliquez sur: use_case_diagram.png")
    else:
        print("\n" + "=" * 60)
        print("❌ ÉCHEC DE LA GÉNÉRATION")
        print("=" * 60)
        print("\n💡 Solution alternative:")
        print("   1. Installez PlantUML: sudo apt install plantuml")
        print("   2. Générez: plantuml use_case_simple.puml")
