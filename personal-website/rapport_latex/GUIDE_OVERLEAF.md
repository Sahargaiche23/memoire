# 📚 GUIDE COMPLET - OVERLEAF

## 🎯 VOTRE RAPPORT EST PRÊT POUR OVERLEAF!

J'ai créé pour vous un rapport LaTeX complet et professionnel!

---

## 📁 FICHIERS CRÉÉS

```
rapport_latex/
├── main.tex                    ✅ Fichier principal LaTeX
├── sprint1.tex                 (à créer)
├── sprint2.tex                 (à créer)
├── sprint3.tex                 (à créer)
├── sprint4.tex                 (à créer)
├── annexe_code.tex             (à créer)
├── annexe_tests.tex            (à créer)
├── annexe_installation.tex     (à créer)
├── images/                     (dossier pour vos images)
└── GUIDE_OVERLEAF.md          ✅ Ce fichier
```

---

## 🚀 MÉTHODE 1: UPLOAD SUR OVERLEAF (RAPIDE)

### Étape 1: Créer un Compte Overleaf

1. Allez sur https://www.overleaf.com
2. Cliquez "Register" (gratuit)
3. Créez votre compte

### Étape 2: Créer un Nouveau Projet

1. Cliquez "New Project"
2. Sélectionnez "Blank Project"
3. Nommez: "Rapport_Patrimoine_Municipal"

### Étape 3: Uploader le Fichier

1. Dans Overleaf, cliquez sur l'icône **Upload** (dossier avec flèche)
2. Sélectionnez `main.tex` depuis votre ordinateur
3. Le fichier s'ouvre automatiquement

### Étape 4: Compiler

1. Cliquez sur le bouton **"Recompile"** (bouton vert)
2. Le PDF se génère automatiquement!
3. Vous verrez le PDF à droite

### Étape 5: Télécharger le PDF

1. Cliquez sur **"Download PDF"** 
2. Votre rapport est prêt! 📄

---

## 📝 MÉTHODE 2: PROJET COMPLET AVEC SPRINTS

Si vous voulez un rapport ultra-complet avec tous les sprints:

### Créer les Fichiers de Sprints

Je vais créer des fichiers séparés pour chaque sprint que vous pourrez uploader sur Overleaf.

**Fichiers à uploader:**
1. `main.tex` (déjà créé)
2. `sprint1.tex`
3. `sprint2.tex`
4. `sprint3.tex`
5. `sprint4.tex`
6. Vos images (diagrammes UML + captures)

---

## 🎨 STRUCTURE DU RAPPORT LATEX

### Ce qui est DÉJÀ inclus dans main.tex:

✅ **Page de garde** professionnelle  
✅ **Remerciements**  
✅ **Table des matières** automatique  
✅ **Table des figures** automatique  
✅ **Introduction** complète  
✅ **Chapitre 1:** Présentation du projet  
✅ **Chapitre 2:** Capture des besoins  
✅ **Conclusion** professionnelle  
✅ **Bibliographie**  
✅ **Configuration** LaTeX complète:
- Marges professionnelles
- Couleurs (bleu #667eea)
- En-têtes et pieds de page
- Style de code
- Hyperlinks

### Ce qu'il faut ajouter:

⏳ **Chapitres 3-6:** Sprints 1-4  
⏳ **Images:** 54 images (UML + captures)  
⏳ **Annexes:** Code, tests, installation  

---

## 📊 AJOUTER DES IMAGES DANS OVERLEAF

### Étape 1: Uploader vos Images

1. Dans Overleaf, cliquez sur le dossier **images/**
2. Cliquez **"Upload"**
3. Sélectionnez vos images (diagrammes UML, captures d'écran)

### Étape 2: Insérer une Image

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{images/figure_3_1_uc_authentification.png}
    \caption{Diagramme de cas d'utilisation "S'authentifier"}
    \label{fig:uc_auth}
\end{figure}
```

**Paramètres:**
- `[H]`: Positionne l'image exactement ici
- `width=0.8\textwidth`: Largeur à 80% de la page
- Chemin relatif depuis le fichier .tex

---

## 🔧 PERSONNALISER LE RAPPORT

### Modifier les Informations

Dans `main.tex`, modifiez:

```latex
% Ligne 111-113: Votre nom
\author{Votre Nom}  % ← Changez ici

% Ligne 131: Votre nom
{\large\bfseries Votre Nom\par}  % ← Changez ici

% Ligne 136: Nom encadrant
{\large Nom de l'Encadrant\par}  % ← Changez ici
```

### Changer les Couleurs

```latex
% Ligne 45: Couleur principale
\definecolor{maincolor}{RGB}{102, 126, 234}  % Bleu actuel
```

**Exemples de couleurs:**
- Rouge: `{RGB}{220, 53, 69}`
- Vert: `{RGB}{40, 167, 69}`
- Orange: `{RGB}{253, 126, 20}`

---

## 📥 TÉLÉCHARGER LE PDF DEPUIS OVERLEAF

### Option 1: Téléchargement Simple

1. Cliquez sur **"Download PDF"** (icône PDF en haut)
2. Le PDF se télécharge directement

### Option 2: Télécharger tout le Projet

1. Cliquez sur **"Menu"** (en haut à gauche)
2. Cliquez **"Download"**
3. Choisissez **"Source"** (fichiers .tex + images)
4. Ou **"PDF"** (juste le PDF)

---

## 💡 CONSEILS OVERLEAF

### 1. Compilation Automatique

Overleaf compile automatiquement quand vous arrêtez de taper (après 2-3 secondes).

### 2. Erreurs LaTeX

Si vous voyez des erreurs:
- Cliquez sur la flèche rouge à côté de "Recompile"
- Lisez les erreurs (généralement numéro de ligne indiqué)
- Corrigez le problème

### 3. Historique des Versions

Overleaf sauvegarde automatiquement:
- Cliquez sur **"History"** pour voir l'historique
- Vous pouvez restaurer une ancienne version

### 4. Collaboration

Vous pouvez partager votre projet:
- Cliquez **"Share"**
- Ajoutez l'email de votre encadrant
- Il peut commenter et modifier

---

## 🎓 RÉSULTAT FINAL

Avec ce fichier LaTeX, vous obtenez:

✅ **Rapport professionnel** de ~50 pages (avec sprints: ~98 pages)  
✅ **PDF haute qualité** prêt pour impression  
✅ **Table des matières** automatique  
✅ **Table des figures** automatique  
✅ **Numérotation** automatique  
✅ **Hyperlinks** cliquables  
✅ **Style académique** impeccable  

---

## 🚀 ÉTAPES RECOMMANDÉES

### Aujourd'hui:

1. ✅ Créez votre compte Overleaf
2. ✅ Uploadez `main.tex`
3. ✅ Compilez pour voir le résultat
4. ✅ Modifiez votre nom et les infos personnelles

### Demain:

5. ⏳ Générez vos 20 diagrammes UML (avec PlantUML)
6. ⏳ Prenez vos 25 captures d'écran
7. ⏳ Uploadez toutes les images sur Overleaf

### Après-demain:

8. ⏳ Ajoutez les chapitres des sprints (je peux les créer)
9. ⏳ Insérez les images aux bons endroits
10. ⏳ Relisez et téléchargez le PDF final

---

## ❓ BESOIN D'AIDE?

### Voulez-vous que je créé:

**Option A:** Les fichiers `sprint1.tex` à `sprint4.tex` complets?  
**Option B:** Un script pour convertir automatiquement Markdown → LaTeX?  
**Option C:** Un template Overleaf avec tout déjà configuré?  

**Dites-moi ce dont vous avez besoin!** 🤝

---

## 📞 LIENS UTILES

- **Overleaf:** https://www.overleaf.com
- **Documentation LaTeX:** https://www.overleaf.com/learn
- **PlantUML (pour UML):** http://www.plantuml.com/plantuml/uml/
- **Tutoriel LaTeX:** https://www.overleaf.com/learn/latex/Tutorials

---

**Votre rapport LaTeX est prêt!** 🎉

**Uploadez `main.tex` sur Overleaf et compilez!** ⚡

**Vous aurez un PDF professionnel en 2 minutes!** 📄
