# 📊 RAPPORT DE PROJET
# Système de Gestion du Patrimoine Municipal

---

**Réalisé par:** [Votre Nom]  
**Encadré par:** [Nom Encadrant]  
**Institution:** [Votre Institution]  
**Date:** Novembre 2025

---

# Table des Matières

## Introduction .................................................... 8

## 1. Présentation du Projet ..................................... 10
- 1.1 Introduction .............................................. 10
- 1.2 Présentation de l'organisme d'accueil ..................... 10
- 1.3 Présentation générale du projet ........................... 11
- 1.4 Présentation du contexte .................................. 11
- 1.5 Définition du problème .................................... 12
- 1.6 Les objectifs adoptés ..................................... 12
- 1.7 Les Outils ................................................ 12
  - 1.7.1 Environnement Matériel ............................... 13
  - 1.7.2 Environnement Logiciel ............................... 13
- 1.8 Outils utilisés ........................................... 14
  - 1.8.1 Outils de modélisation ............................... 14
  - 1.8.2 Outil de rédaction du rapport ........................ 14
  - 1.8.3 Outils de développement .............................. 14
- 1.9 Architecture MicroService ................................. 18
  - 1.9.1 Définition ........................................... 18
- 1.10 Méthodologie de conception ............................... 19
  - 1.10.1 La méthode agile - SCRUM ............................ 20
- 1.11 Conclusion ............................................... 22

## 2. Capture des Besoins ....................................... 23
- 2.1 Introduction .............................................. 23
- 2.2 Spécification des besoins ................................. 23
  - 2.2.1 Les besoins fonctionnels ............................. 23
  - 2.2.2 Les besoins non fonctionnels ......................... 24
- 2.3 Benchmarking .............................................. 24
  - 2.3.1 C'est quoi le benchmarking ? ......................... 24
  - 2.3.2 Pourquoi faire un benchmarking ? ..................... 25
  - 2.3.3 Les points forts et faibles des concurrents .......... 26
- 2.4 Diagramme de cas d'utilisation ............................ 27
  - 2.4.1 Classement des cas d'utilisation ..................... 28
- 2.5 Backlog du produit ........................................ 28
  - 2.5.1 Équipe et rôle ....................................... 28
  - 2.5.2 Backlog du produit ................................... 28
  - 2.5.3 Planification des Sprints ............................ 31
- 2.6 Architecture de l'application ............................. 32
  - 2.6.1 Conclusion ........................................... 33

## 3. Sprint 1 : Administrateur ................................. 34
- 3.1 Introduction .............................................. 34
- 3.2 Spécification de besoins du Sprint 1 ...................... 34
- 3.3 Analyse ................................................... 35
  - 3.3.1 Raffinement du cas d'utilisation "Gérer les actifs" .. 36
  - 3.3.2 Raffinement du cas d'utilisation "Gérer les catégories" 37
  - 3.3.3 Diagramme de séquence ................................ 37
  - 3.3.4 Diagramme de séquence "Authentification" ............. 39
- 3.4 Conception ................................................ 39
  - 3.4.1 Diagramme de séquence détaillé ....................... 39
- 3.5 Implémentation ............................................ 40
  - 3.5.1 Les interfaces relatives au Sprint 1 ................. 40
  - 3.5.2 Burndown Chart ....................................... 42
- 3.6 Conclusion ................................................ 42

## 4. Sprint 2 : Gestionnaire d'Actifs .......................... 43
- 4.1 Introduction .............................................. 43
- 4.2 Sprint Backlog ............................................ 43
- 4.3 Analyse ................................................... 44
  - 4.3.1 Description textuelle du cas d'utilisation ........... 45
- 4.4 Conception ................................................ 49
  - 4.4.1 Conception du cas d'utilisation "Ajouter un actif" ... 50
  - 4.4.2 Conception du cas d'utilisation "Planifier maintenance" 51
  - 4.4.3 Diagramme de classe du Sprint 2 ...................... 52
  - 4.4.4 Diagramme d'activité "Gérer maintenance" ............. 54
- 4.5 Implémentation et tests ................................... 55
  - 4.5.1 Le schéma de la base de données du Sprint 2 .......... 55
  - 4.5.2 Les interfaces ....................................... 56
  - 4.5.3 Tests de validation .................................. 63
  - 4.5.4 Tests avec Postman ................................... 64
  - 4.5.5 Burndown Chart ....................................... 66
- 4.6 Conclusion ................................................ 66

## 5. Sprint 3 : Gestion des Maintenances ....................... 67
- 5.1 Introduction .............................................. 67
- 5.2 Sprint Backlog ............................................ 67
- 5.3 Analyse ................................................... 67
  - 5.3.1 Diagramme d'activité "Suivre maintenance" ............ 71
- 5.4 Conception ................................................ 72
  - 5.4.1 Diagramme de classe .................................. 72
- 5.5 Implémentation ............................................ 72
  - 5.5.1 Les interfaces ....................................... 72
  - 5.5.2 Schéma de la base de données du Sprint 3 ............. 77
  - 5.5.3 Tests de validation .................................. 78
  - 5.5.4 Tests avec Postman ................................... 79
  - 5.5.5 Burndown Chart ....................................... 81
- 5.6 Conclusion ................................................ 81

## 6. Sprint 4 : Alertes et Messagerie .......................... 82
- 6.1 Introduction .............................................. 82
- 6.2 Sprint Backlog du Sprint 4 ................................ 82
  - 6.2.1 Diagramme de cas d'utilisation "Messagerie" .......... 83
- 6.3 Analyse du Sprint 4 ....................................... 83
  - 6.3.1 Analyse de CU "Envoyer message" ...................... 87
- 6.4 Conception ................................................ 88
  - 6.4.1 Diagramme de classe Sprint 4 ......................... 88
  - 6.4.2 Diagrammes de séquences détaillés .................... 90
- 6.5 Implémentation ............................................ 91
  - 6.5.1 Schéma de la base de données du sprint 4 ............. 91
  - 6.5.2 Les interfaces ....................................... 92
  - 6.5.3 Tests ................................................ 95
  - 6.5.4 Burndown Chart ....................................... 97
- 6.6 Conclusion ................................................ 97
- 6.7 Conclusion générale ....................................... 98

---

# Table des Figures

- 1.1 Logo Patrimoine Municipal ................................. 11
- 1.2 Architecture MicroService .................................. 18
- 1.3 Architecture Frontend/Backend .............................. 19
- 1.4 Les étapes d'une méthode agile ............................ 20
- 1.5 SCRUM Méthodologie ........................................ 21
- 1.6 SCRUM Board ............................................... 22

- 2.1 Principaux concurrents du marché .......................... 24
- 2.2 Diagramme CU global ....................................... 28
- 2.3 Diagramme de déploiement .................................. 33

- 3.1 Diagramme de cas d'utilisation Administrateur ............. 35
- 3.2 Raffinement "Gérer les actifs" ............................ 36
- 3.3 Raffinement "Gérer les catégories" ........................ 37
- 3.4 Diagramme de séquence "Authentification" .................. 38
- 3.5 Diagramme de classe Sprint 1 .............................. 39
- 3.6 Diagramme de séquence détaillé "Ajouter actif" ............ 39
- 3.7 Page de connexion ......................................... 40
- 3.8 Dashboard administrateur .................................. 40
- 3.9 Consulter liste des actifs ................................ 41
- 3.10 Ajouter un actif ......................................... 41
- 3.11 Burndown Chart Sprint 1 .................................. 42

- 4.1 Diagramme de Cas d'utilisation Gestionnaire ............... 44
- 4.2 Diagramme de Raffinement "Gérer actif" .................... 45
- 4.3 Diagramme de Raffinement "Consulter les actifs" ........... 46
- 4.4 Raffinement du CU "Planifier maintenance" ................. 47
- 4.5 Diagramme de Raffinement "Consulter maintenances" ......... 48
- 4.6 Diagramme de Raffinement "Générer rapport" ................ 49
- 4.7 Diagramme de séquence "Ajouter actif" ..................... 50
- 4.8 Diagramme de séquence "Planifier maintenance" ............. 52
- 4.9 Diagramme de classe du Sprint 2 ........................... 54
- 4.10 Diagramme d'activité "Gérer maintenance" ................. 54
- 4.11 Schéma base de données Sprint 2 .......................... 56
- 4.12 Page liste des actifs .................................... 57
- 4.13 Page détails actif ....................................... 57
- 4.14 Page planifier maintenance ............................... 58
- 4.15 Page liste maintenances .................................. 58
- 4.16 Page détails maintenance ................................. 59
- 4.17 Page consulter historique ................................ 59
- 4.18 Page générer rapport ..................................... 60
- 4.19 Test Postman GET /api/assets ............................. 63
- 4.20 Test Postman POST /api/maintenances ...................... 64
- 4.21 Burndown Chart Sprint 2 .................................. 66

- 5.1 Cas d'utilisation Gestion Maintenances .................... 68
- 5.2 Diagramme de Raffinement "Suivre maintenances" ............ 69
- 5.3 Diagramme de Raffinement "Consulter alertes" .............. 70
- 5.4 Diagramme d'activité "Suivre maintenance" ................. 71
- 5.5 Diagramme de classe du Sprint 3 ........................... 72
- 5.6 Page tableau de bord maintenances ......................... 73
- 5.7 Page modifier statut maintenance .......................... 73
- 5.8 Page consulter alertes dynamiques ......................... 74
- 5.9 Page mouvements d'actifs .................................. 74
- 5.10 Page historique maintenances ............................. 75
- 5.11 Page statistiques ........................................ 75
- 5.12 Schéma base de données Sprint 3 .......................... 77
- 5.13 Test Postman GET /api/alerts ............................. 79
- 5.14 Test Postman PUT /api/maintenances/:id/status ............ 80
- 5.15 Burndown Chart Sprint 3 .................................. 81

- 6.1 Diagramme de cas d'utilisation "Messagerie" ............... 83
- 6.2 Diagramme de Raffinement "Gérer messagerie" ............... 84
- 6.3 Diagramme de Raffinement "Créer groupe" ................... 84
- 6.4 Diagramme des classes participantes "Messagerie" .......... 85
- 6.5 Diagramme de séquence "Envoyer message" ................... 86
- 6.6 Diagramme de séquence "Créer groupe" ...................... 87
- 6.7 Diagramme de séquence détaillé "Chat" ..................... 88
- 6.8 Diagramme de classe Sprint 4 .............................. 89
- 6.9 Diagramme de séquence détaillé cas d'utilisation "Message" 90
- 6.10 Schéma base de données Sprint 4 .......................... 91
- 6.11 Interface messagerie principale .......................... 92
- 6.12 Interface conversation 1-1 ............................... 92
- 6.13 Interface groupe de discussion ........................... 93
- 6.14 Interface créer groupe ................................... 93
- 6.15 Interface notifications .................................. 94
- 6.16 Test Postman POST /api/messages .......................... 95
- 6.17 Test Postman GET /api/groups ............................. 96
- 6.18 Test Postman POST /api/groups/:id/messages ............... 96
- 6.19 Burndown Chart Sprint 4 .................................. 97

---

