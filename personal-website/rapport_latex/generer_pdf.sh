#!/bin/bash

# ============================================================
# SCRIPT DE GÉNÉRATION PDF - Rapport Patrimoine Municipal
# ============================================================

echo "🚀 Génération du PDF en cours..."
echo ""

# Vérifier si pdflatex est installé
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex n'est pas installé!"
    echo ""
    echo "Pour installer LaTeX sur Linux:"
    echo "  sudo apt-get install texlive-full"
    echo ""
    echo "Ou utilisez Overleaf (recommandé):"
    echo "  https://www.overleaf.com"
    echo ""
    exit 1
fi

# Compilation LaTeX
echo "📝 Compilation LaTeX (étape 1/3)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "📝 Compilation LaTeX (étape 2/3)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "📝 Compilation LaTeX (étape 3/3)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# Vérifier si le PDF a été généré
if [ -f "main.pdf" ]; then
    echo ""
    echo "✅ PDF généré avec succès!"
    echo "📄 Fichier: main.pdf"
    echo ""
    
    # Renommer le PDF
    mv main.pdf Rapport_Patrimoine_Municipal.pdf
    echo "✅ PDF renommé: Rapport_Patrimoine_Municipal.pdf"
    echo ""
    
    # Nettoyer les fichiers temporaires
    echo "🧹 Nettoyage des fichiers temporaires..."
    rm -f *.aux *.log *.toc *.out *.lof *.lot
    
    echo ""
    echo "🎉 Terminé!"
    echo ""
    echo "📁 Votre rapport est prêt dans:"
    echo "   $(pwd)/Rapport_Patrimoine_Municipal.pdf"
    echo ""
    
else
    echo ""
    echo "❌ Erreur lors de la génération du PDF"
    echo ""
    echo "Consultez les logs:"
    echo "  cat main.log"
    echo ""
    echo "💡 Solution alternative: Utilisez Overleaf"
    echo "   https://www.overleaf.com"
    echo ""
    exit 1
fi
