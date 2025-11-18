#!/bin/bash

echo "🧹 Nettoyage complet du cache et rebuild..."

# Arrêter les serveurs en cours
echo "⏹️  Arrêt des serveurs..."
pkill -f "npm start"
pkill -f "python3 app.py"
sleep 2

# Nettoyer le cache frontend
echo "🧹 Nettoyage cache React..."
cd frontend
rm -rf node_modules/.cache
rm -rf build
rm -rf .cache
npm cache clean --force

# Rebuild frontend
echo "🔨 Rebuild frontend..."
npm run build 2>/dev/null || echo "Build n'est pas nécessaire pour dev"

# Redémarrer backend
echo "🚀 Démarrage backend..."
cd ../backend
python3 app.py &
BACKEND_PID=$!
sleep 3

# Redémarrer frontend
echo "🚀 Démarrage frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Serveurs redémarrés!"
echo "📝 Backend PID: $BACKEND_PID"
echo "📝 Frontend PID: $FRONTEND_PID"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:5000"
echo ""
echo "⚠️  IMPORTANT:"
echo "   1. Ouvrir Chrome/Firefox"
echo "   2. Appuyer Ctrl+Shift+Delete"
echo "   3. Cocher 'Images et fichiers en cache'"
echo "   4. Cliquer 'Effacer les données'"
echo "   5. Appuyer Ctrl+Shift+R pour forcer le rechargement"
echo ""
