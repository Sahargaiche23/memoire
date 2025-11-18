#!/bin/bash
# Script de test de modification de profil

echo "🔐 ÉTAPE 1: Connexion..."
read -p "Entrez votre mot de passe: " PASSWORD

# Connexion
RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"sahar\", \"password\": \"$PASSWORD\"}")

echo "Réponse login: $RESPONSE"

# Extraire le token
TOKEN=$(echo $RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ ERREUR: Pas de token reçu. Vérifiez votre mot de passe!"
    exit 1
fi

echo "✅ Token reçu: ${TOKEN:0:20}..."
echo ""

# Modification
echo "📝 ÉTAPE 2: Modification du profil..."
UPDATE_RESPONSE=$(curl -s -X PUT http://localhost:5000/api/users/7 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "full_name": "Sahar Gaiche Updated",
    "email": "sahar.updated@test.com"
  }')

echo "Réponse update: $UPDATE_RESPONSE"
echo ""

# Vérification
echo "🔍 ÉTAPE 3: Vérification en base de données..."
sqlite3 instance/patrimoine.db "SELECT username, full_name, email FROM users WHERE id=7;"

echo ""
echo "✅ Test terminé!"
