#!/bin/bash

echo ""
echo "======================================================================"
echo "🚀 DÉMARRAGE ET TEST COMPLET - Profil et Upload d'Image"
echo "======================================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier si le backend est déjà en cours
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}✅ Backend déjà en cours d'exécution sur le port 5000${NC}"
else
    echo -e "${RED}❌ Backend n'est pas en cours d'exécution${NC}"
    echo -e "${YELLOW}⚠️  Démarrez le backend dans un terminal séparé:${NC}"
    echo "   cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend"
    echo "   source /home/sahar/Bureau/Stage/venv/bin/activate"
    echo "   python3 app.py"
    echo ""
    exit 1
fi

# Vérifier si le frontend est déjà en cours
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}✅ Frontend déjà en cours d'exécution sur le port 3000${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend n'est pas en cours d'exécution${NC}"
    echo -e "${YELLOW}   Pour tester l'interface web, démarrez le frontend:${NC}"
    echo "   cd ~/Bureau/ERPM2/CascadeProjects/personal-website/frontend"
    echo "   npm start"
    echo ""
fi

echo ""
echo "======================================================================"
echo "🧪 TESTS AUTOMATIQUES"
echo "======================================================================"
echo ""

cd ~/Bureau/ERPM2/CascadeProjects/personal-website/backend

# Test 1: Test de connexion simple
echo "📝 TEST 1: Connexion au backend"
echo "----------------------------------------------------------------------"

RESPONSE=$(curl -s -w "%{http_code}" -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "sahar", "password": "test123"}')

HTTP_CODE="${RESPONSE: -3}"
BODY="${RESPONSE:0:${#RESPONSE}-3}"

if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✅ Connexion réussie!${NC}"
    echo "   Response code: $HTTP_CODE"
else
    echo -e "${RED}❌ Erreur de connexion!${NC}"
    echo "   Response code: $HTTP_CODE"
    echo "   Response: $BODY"
    exit 1
fi

echo ""

# Test 2: Vérification base de données
echo "📝 TEST 2: Vérification de la base de données"
echo "----------------------------------------------------------------------"

echo "Structure de la table users:"
sqlite3 instance/patrimoine.db "PRAGMA table_info(users);" | grep -E "profile_image|full_name|email"

echo ""
echo "Utilisateur 'sahar' actuel:"
sqlite3 instance/patrimoine.db "SELECT id, username, full_name, email, profile_image FROM users WHERE username='sahar';"

echo ""

# Test 3: Test complet avec Python
echo "📝 TEST 3: Tests complets (modification + upload)"
echo "----------------------------------------------------------------------"

source /home/sahar/Bureau/Stage/venv/bin/activate
python3 test_profile_complet.py

echo ""
echo "======================================================================"
echo "📋 INSTRUCTIONS POUR TEST MANUEL"
echo "======================================================================"
echo ""
echo "1. Ouvrez votre navigateur: http://localhost:3000"
echo ""
echo "2. Connectez-vous avec:"
echo "   Username: sahar"
echo "   Password: test123"
echo ""
echo "3. Allez à la page Profile"
echo ""
echo "4. Testez la modification:"
echo "   - Cliquez 'Modifier le Profil'"
echo "   - Changez le nom et l'email"
echo "   - Cliquez 'Enregistrer'"
echo "   - Vérifiez que les données s'affichent"
echo ""
echo "5. Testez l'upload d'image:"
echo "   - Cliquez sur l'avatar"
echo "   - Sélectionnez une image"
echo "   - Vérifiez que l'image s'affiche"
echo ""
echo "6. Testez la persistance:"
echo "   - Déconnectez-vous"
echo "   - Reconnectez-vous"
echo "   - Vérifiez que tout est toujours là"
echo ""
echo "======================================================================"
echo ""

# Vérifier les images uploadées
if [ -d "uploads" ]; then
    IMAGE_COUNT=$(ls -1 uploads/profile_* 2>/dev/null | wc -l)
    if [ "$IMAGE_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ $IMAGE_COUNT image(s) de profil trouvée(s):${NC}"
        ls -lh uploads/profile_* 2>/dev/null
    else
        echo -e "${YELLOW}⚠️  Aucune image de profil trouvée${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Dossier uploads/ n'existe pas${NC}"
fi

echo ""
echo "======================================================================"
echo -e "${GREEN}✅ Tests terminés!${NC}"
echo "======================================================================"
echo ""
