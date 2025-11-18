# 📐 TOUS LES DIAGRAMMES UML - PRÊTS À GÉNÉRER

## 🎯 INSTRUCTIONS RAPIDES

Pour chaque diagramme ci-dessous:

1. **Copiez** le code entre `@startuml` et `@enduml`
2. **Allez sur:** http://www.plantuml.com/plantuml/uml/
3. **Collez** le code dans l'éditeur
4. **Cliquez** sur le diagramme généré
5. **Téléchargez** l'image PNG
6. **Renommez** selon le nom indiqué

---

## 📊 ARCHITECTURE GÉNÉRALE

### Figure 1.1: Architecture MicroService

**Nom fichier:** `figure_1_1_architecture_microservice.png`

```plantuml
@startuml
!define RECTANGLE class

skinparam backgroundColor #FFFFFF
skinparam rectangle {
    BackgroundColor<<frontend>> #E3F2FD
    BackgroundColor<<backend>> #E8F5E9
    BackgroundColor<<database>> #FFF3E0
    BorderColor #1976D2
    FontSize 12
}

rectangle "CLIENT (Navigateur)\nReact 18.2\nPort 3000" as Client <<frontend>> {
}

rectangle "BACKEND API (Flask)\nPort 5000" as Backend <<backend>> {
    rectangle "Authentication Service\n(JWT)" as Auth
    rectangle "Assets Service\n(/api/assets)" as Assets
    rectangle "Maintenances Service\n(/api/maintenances)" as Maint
    rectangle "Alerts Service\n(/api/alerts)" as Alerts
    rectangle "Messages Service\n(/api/messages)" as Messages
    rectangle "Statistics Service\n(/api/statistics)" as Stats
}

rectangle "BASE DE DONNÉES\nSQLite / PostgreSQL" as DB <<database>> {
    rectangle "Users" as TUsers
    rectangle "Assets" as TAssets
    rectangle "Maintenances" as TMaint
    rectangle "Messages" as TMessages
}

Client -down-> Backend : HTTP/REST API\nJSON
Backend -down-> DB : SQLAlchemy ORM

note right of Client
  Technologies:
  - React Router
  - Axios
  - Recharts
  - JWT Auth
end note

note right of Backend
  Technologies:
  - Flask 3.0
  - Flask-JWT-Extended
  - Flask-CORS
  - SQLAlchemy 2.0
end note

@enduml
```

---

## 📦 CHAPITRE 2: CAPTURE DES BESOINS

### Figure 2.1: Diagramme de Cas d'Utilisation GLOBAL

**Nom fichier:** `figure_2_1_uc_global.png`

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Administrateur" as Admin
actor "Gestionnaire" as Manager
actor "Technicien" as Tech
actor "Utilisateur" as User

rectangle "Système Gestion Patrimoine Municipal" {
  
  package "Gestion Utilisateurs" {
    usecase "Gérer utilisateurs" as UC1
    usecase "Gérer catégories" as UC2
  }
  
  package "Gestion Actifs" {
    usecase "Gérer actifs" as UC3
    usecase "Ajouter actif" as UC4
    usecase "Modifier actif" as UC5
    usecase "Supprimer actif" as UC6
    usecase "Consulter actifs" as UC7
  }
  
  package "Gestion Maintenances" {
    usecase "Planifier maintenance" as UC8
    usecase "Consulter maintenances" as UC9
    usecase "Mettre à jour statut" as UC10
  }
  
  package "Alertes" {
    usecase "Consulter alertes" as UC11
    usecase "Voir statistiques" as UC12
  }
  
  package "Messagerie" {
    usecase "Envoyer message" as UC13
    usecase "Créer groupe" as UC14
  }
  
  package "Authentification" {
    usecase "S'authentifier" as UC0
  }
}

Admin --> UC1
Admin --> UC2
Admin --> UC12

Manager --> UC3
UC3 ..> UC4 : <<extend>>
UC3 ..> UC5 : <<extend>>
UC3 ..> UC6 : <<extend>>
UC3 ..> UC7 : <<include>>

Manager --> UC8
Manager --> UC9
Manager --> UC11

Tech --> UC10
Tech --> UC9

User --> UC13
User --> UC14
User --> UC0

@enduml
```

---

### Figure 2.2: Diagramme de Déploiement

**Nom fichier:** `figure_2_2_deploiement.png`

```plantuml
@startuml
!define NODE rectangle

skinparam node {
    BackgroundColor #E3F2FD
    BorderColor #1976D2
}

node "Poste Client" {
    component "Navigateur Web" as Browser {
        component "Application React" as ReactApp
    }
}

node "Serveur Web\n(Netlify / Vercel)" {
    component "Frontend\nReact Build" as Frontend
}

node "Serveur Application\n(Render / Heroku)" {
    component "Backend\nFlask API" as Backend {
        component "Routes API" as Routes
        component "JWT Auth" as JWT
        component "Business Logic" as Logic
    }
}

node "Serveur Base de Données\n(PostgreSQL)" {
    database "patrimoine_db" as DB {
        storage "users" as T1
        storage "assets" as T2
        storage "maintenances" as T3
        storage "messages" as T4
    }
}

ReactApp --> Frontend : HTTP/HTTPS
Frontend --> Backend : REST API\nJSON
Backend --> DB : TCP/IP\nPort 5432

@enduml
```

---

## 🔐 SPRINT 1: ADMINISTRATEUR

### Figure 3.1: Cas d'Utilisation "S'authentifier"

**Nom fichier:** `figure_3_1_uc_authentification.png`

```plantuml
@startuml
left to right direction

actor "Utilisateur" as User

rectangle "Authentification" {
  usecase "S'authentifier" as UC1
  usecase "Saisir identifiants" as UC2
  usecase "Valider identifiants" as UC3
  usecase "Générer token JWT" as UC4
  usecase "Rediriger dashboard" as UC5
}

User --> UC1

UC1 ..> UC2 : <<include>>
UC1 ..> UC3 : <<include>>
UC1 ..> UC4 : <<include>>
UC1 ..> UC5 : <<include>>

note right of UC1
  Précondition:
  - Utilisateur a un compte
  
  Postcondition:
  - Utilisateur authentifié
  - Token JWT stocké
end note

@enduml
```

---

### Figure 3.2: Cas d'Utilisation "Gérer Utilisateurs"

**Nom fichier:** `figure_3_2_uc_gerer_utilisateurs.png`

```plantuml
@startuml
left to right direction

actor "Administrateur" as Admin

rectangle "Gestion des Utilisateurs" {
  usecase "Gérer utilisateurs" as UC1
  usecase "Ajouter utilisateur" as UC2
  usecase "Modifier utilisateur" as UC3
  usecase "Supprimer utilisateur" as UC4
  usecase "Consulter liste" as UC5
  usecase "Rechercher utilisateur" as UC6
}

Admin --> UC1

UC1 ..> UC2 : <<extend>>
UC1 ..> UC3 : <<extend>>
UC1 ..> UC4 : <<extend>>
UC1 ..> UC5 : <<include>>
UC1 ..> UC6 : <<extend>>

@enduml
```

---

### Figure 3.3: Séquence "Authentification"

**Nom fichier:** `figure_3_3_seq_authentification.png`

```plantuml
@startuml
skinparam sequenceArrowThickness 2
skinparam roundcorner 20
skinparam maxmessagesize 100

actor "Utilisateur" as User
participant "Page Login" as Login
participant "API Backend" as API
database "Base de Données" as DB

User -> Login: Accède à /login
activate Login
Login --> User: Affiche formulaire

User -> Login: Saisit email + password
User -> Login: Clique "Se connecter"

Login -> API: POST /api/login\n{email, password}
activate API

API -> DB: SELECT * FROM users\nWHERE email = ?
activate DB
DB --> API: Retourne utilisateur
deactivate DB

alt Identifiants valides
    API -> API: Vérifie password (bcrypt)
    API -> API: Génère token JWT
    API --> Login: 200 OK\n{token, user}
    Login -> Login: Stocke token (localStorage)
    Login -> Login: Stocke user (localStorage)
    Login --> User: Redirige vers /dashboard
    note right: Authentification réussie
else Identifiants invalides
    API --> Login: 401 Unauthorized\n{error: "Invalid credentials"}
    Login --> User: Affiche message erreur
    note right: Échec authentification
end

deactivate API
deactivate Login

@enduml
```

---

### Figure 3.4: Séquence "Créer Utilisateur"

**Nom fichier:** `figure_3_4_seq_creer_utilisateur.png`

```plantuml
@startuml
actor "Admin" as Admin
participant "Page Utilisateurs" as UI
participant "API Backend" as API
database "Base de Données" as DB

Admin -> UI: Clique "Ajouter Utilisateur"
activate UI
UI --> Admin: Affiche formulaire

Admin -> UI: Remplit formulaire\n(nom, email, rôle, password)
Admin -> UI: Clique "Enregistrer"

UI -> UI: Valide formulaire côté client
UI -> API: POST /api/users\n{full_name, email, role, password}
activate API

API -> API: Valide données
API -> API: Hash password (bcrypt)

API -> DB: INSERT INTO users\n(full_name, email, role, password_hash)
activate DB
DB --> API: Retourne user créé (id, ...)
deactivate DB

API --> UI: 201 Created\n{user}
UI -> UI: Ajoute user à la liste
UI --> Admin: Affiche notification succès\n"Utilisateur créé"

deactivate API
deactivate UI

@enduml
```

---

### Figure 3.5: Séquence "Dashboard Statistiques"

**Nom fichier:** `figure_3_5_seq_dashboard.png`

```plantuml
@startuml
actor "Admin" as Admin
participant "Dashboard UI" as UI
participant "API /statistics" as StatsAPI
participant "API /alerts" as AlertsAPI
database "Base de Données" as DB

Admin -> UI: Accède à /dashboard
activate UI

par Chargement parallèle des données
    UI -> StatsAPI: GET /api/statistics
    activate StatsAPI
    StatsAPI -> DB: SELECT COUNT(*) FROM assets
    StatsAPI -> DB: SELECT COUNT(*) WHERE status='actif'
    StatsAPI -> DB: SELECT SUM(value) FROM assets
    StatsAPI -> DB: SELECT category, COUNT(*)\nGROUP BY category
    DB --> StatsAPI: Retourne statistiques
    StatsAPI --> UI: 200 OK\n{stats}
    deactivate StatsAPI
else
    UI -> AlertsAPI: GET /api/alerts
    activate AlertsAPI
    AlertsAPI -> DB: Query maintenances urgentes
    AlertsAPI -> DB: Query maintenances en retard
    AlertsAPI -> DB: Query actifs maintenance_required
    DB --> AlertsAPI: Retourne données
    AlertsAPI -> AlertsAPI: Génère alertes dynamiques
    AlertsAPI --> UI: 200 OK\n{alerts[]}
    deactivate AlertsAPI
end

UI -> UI: Génère graphiques\n(Recharts Pie + Bar)
UI --> Admin: Affiche dashboard complet\n(stats + graphs + alerts)

deactivate UI

@enduml
```

---

### Figure 3.6: Diagramme de Classes Sprint 1

**Nom fichier:** `figure_3_6_classes_sprint1.png`

```plantuml
@startuml
skinparam classAttributeIconSize 0

class User {
  - id: Integer {PK}
  - full_name: String
  - email: String {unique}
  - password_hash: String
  - role: String
  - created_at: DateTime
  __
  + __init__(full_name, email, role)
  + to_dict(): dict
  + check_password(password): Boolean
  + set_password(password): void
}

class Category {
  - id: Integer {PK}
  - name: String {unique}
  - description: String
  - created_at: DateTime
  __
  + __init__(name, description)
  + to_dict(): dict
}

class Asset {
  - id: Integer {PK}
  - name: String
  - category_id: Integer {FK}
  - description: String
  - purchase_date: Date
  - value: Float
  - location: String
  - status: String
  - created_at: DateTime
  __
  + __init__(...)
  + to_dict(): dict
}

User "1" -- "*" Asset : crée >
Category "1" -- "*" Asset : classe >

note right of User
  Rôles possibles:
  - admin
  - manager
  - technician
end note

note bottom of Asset
  Status possibles:
  - actif
  - en_maintenance
  - hors_service
  - maintenance_required
end note

@enduml
```

---

## 📦 SPRINT 2: GESTIONNAIRE D'ACTIFS

### Figure 4.1: Cas d'Utilisation Gestionnaire

**Nom fichier:** `figure_4_1_uc_gestionnaire.png`

```plantuml
@startuml
left to right direction

actor "Gestionnaire" as Manager

rectangle "Gestion des Actifs" {
  usecase "Gérer actifs" as UC1
  usecase "Ajouter actif" as UC2
  usecase "Modifier actif" as UC3
  usecase "Supprimer actif" as UC4
  usecase "Consulter actifs" as UC5
  usecase "Rechercher actif" as UC6
  usecase "Filtrer actifs" as UC7
}

rectangle "Gestion Maintenances" {
  usecase "Planifier maintenance" as UC8
  usecase "Consulter maintenances" as UC9
  usecase "Modifier maintenance" as UC10
}

Manager --> UC1
UC1 ..> UC2 : <<extend>>
UC1 ..> UC3 : <<extend>>
UC1 ..> UC4 : <<extend>>
UC1 ..> UC5 : <<include>>
UC1 ..> UC6 : <<extend>>
UC1 ..> UC7 : <<extend>>

Manager --> UC8
Manager --> UC9
Manager --> UC10

@enduml
```

---

### Figure 4.2: Diagramme de Classes Sprint 2

**Nom fichier:** `figure_4_2_classes_sprint2.png`

```plantuml
@startuml
skinparam classAttributeIconSize 0

class Asset {
  - id: Integer {PK}
  - name: String
  - category_id: Integer {FK}
  - description: String
  - purchase_date: Date
  - value: Float
  - location: String
  - status: String
  - created_at: DateTime
  __
  + to_dict(): dict
}

class Maintenance {
  - id: Integer {PK}
  - asset_id: Integer {FK}
  - maintenance_type: String
  - scheduled_date: Date
  - completed_date: Date
  - description: String
  - cost: Float
  - status: String
  - created_at: DateTime
  __
  + to_dict(): dict
}

class Category {
  - id: Integer {PK}
  - name: String
  - description: String
}

Asset "1" -- "*" Maintenance : nécessite >
Category "1" -- "*" Asset : classe >

note right of Maintenance
  Types:
  - preventive
  - corrective
  
  Status:
  - planifié
  - en_cours
  - terminé
  - annulé
end note

@enduml
```

---

### Figure 4.3: Séquence "Ajouter Actif"

**Nom fichier:** `figure_4_3_seq_ajouter_actif.png`

```plantuml
@startuml
actor "Gestionnaire" as Manager
participant "Page Actifs" as UI
participant "API Backend" as API
database "Base de Données" as DB

Manager -> UI: Clique "Ajouter Actif"
activate UI
UI --> Manager: Affiche formulaire

Manager -> UI: Remplit formulaire\n(nom, catégorie, valeur, etc.)
Manager -> UI: Clique "Enregistrer"

UI -> UI: Valide formulaire
UI -> API: POST /api/assets\n{name, category_id, value, ...}
activate API

API -> API: Valide données
API -> DB: INSERT INTO assets\n(name, category_id, value, status, ...)
activate DB
DB --> API: Retourne asset créé
deactivate DB

API --> UI: 201 Created\n{asset}
UI -> UI: Ajoute asset à la liste
UI --> Manager: Affiche notification\n"Actif ajouté avec succès"

deactivate API
deactivate UI

@enduml
```

---

### Figure 4.4: Séquence "Planifier Maintenance"

**Nom fichier:** `figure_4_4_seq_planifier_maintenance.png`

```plantuml
@startuml
actor "Gestionnaire" as Manager
participant "Page Maintenances" as UI
participant "API Backend" as API
database "Base de Données" as DB

Manager -> UI: Clique "Planifier Maintenance"
activate UI
UI --> Manager: Affiche formulaire

Manager -> UI: Sélectionne actif
Manager -> UI: Remplit détails\n(type, date, description)
Manager -> UI: Clique "Planifier"

UI -> API: POST /api/maintenances\n{asset_id, type, scheduled_date, ...}
activate API

API -> DB: INSERT INTO maintenances\n(asset_id, type, scheduled_date, status='planifié')
activate DB
DB --> API: Retourne maintenance créée
deactivate DB

API --> UI: 201 Created\n{maintenance}
UI --> Manager: Confirmation\n"Maintenance planifiée"

deactivate API
deactivate UI

note right of DB
  Cette maintenance générera
  automatiquement une alerte
  si date ≤ 7 jours
end note

@enduml
```

---

## 🔧 SPRINT 3: GESTION MAINTENANCES

### Figure 5.1: Cas d'Utilisation Maintenances

**Nom fichier:** `figure_5_1_uc_maintenances.png`

```plantuml
@startuml
left to right direction

actor "Gestionnaire" as Manager
actor "Technicien" as Tech

rectangle "Gestion Maintenances" {
  usecase "Consulter alertes dynamiques" as UC1
  usecase "Mettre à jour statut" as UC2
  usecase "Consulter statistiques" as UC3
  usecase "Enregistrer mouvements" as UC4
  usecase "Consulter historique" as UC5
}

Manager --> UC1
Manager --> UC3
Manager --> UC4
Manager --> UC5

Tech --> UC2
Tech --> UC5

note right of UC1
  Alertes générées automatiquement:
  - Maintenances urgentes (≤7j)
  - Maintenances en retard
  - Actifs nécessitant maintenance
end note

@enduml
```

---

### Figure 5.2: Diagramme de Classes Sprint 3

**Nom fichier:** `figure_5_2_classes_sprint3.png`

```plantuml
@startuml
skinparam classAttributeIconSize 0

class Alert {
  - id: String {dynamic}
  - asset_id: Integer
  - alert_type: String
  - message: String
  - due_date: Date
  - is_read: Boolean
  - created_at: DateTime
  - source: String
  __
  + generate_from_maintenance(): Alert
  + generate_from_asset(): Alert
}

class Maintenance {
  - id: Integer {PK}
  - asset_id: Integer {FK}
  - status: String
  - scheduled_date: Date
  - completed_date: Date
  __
  + is_urgent(): Boolean
  + is_overdue(): Boolean
  + days_until(): Integer
}

class Asset {
  - id: Integer {PK}
  - status: String
  __
  + needs_maintenance(): Boolean
}

Alert ..> Maintenance : génère depuis >
Alert ..> Asset : génère depuis >

note bottom of Alert
  Alertes 100% dynamiques
  (non stockées en DB)
  
  Types d'ID:
  - "maintenance-{id}"
  - "overdue-{id}"
  - "asset-{id}"
end note

@enduml
```

---

### Figure 5.3: Séquence "Consulter Alertes Dynamiques"

**Nom fichier:** `figure_5_3_seq_alertes.png`

```plantuml
@startuml
actor "Utilisateur" as User
participant "Dashboard UI" as UI
participant "API /alerts" as API
database "Base de Données" as DB

User -> UI: Accède au Dashboard
activate UI

UI -> API: GET /api/alerts
activate API

API -> API: today = date.today()
API -> API: next_week = today + 7 days

API -> DB: SELECT * FROM maintenances\nWHERE status='planifié'\nAND scheduled_date BETWEEN today AND next_week
activate DB
DB --> API: urgent_maintenances[]
deactivate DB

API -> DB: SELECT * FROM maintenances\nWHERE status='planifié'\nAND scheduled_date < today
activate DB
DB --> API: overdue_maintenances[]
deactivate DB

API -> DB: SELECT * FROM assets\nWHERE status='maintenance_required'
activate DB
DB --> API: assets_need_maintenance[]
deactivate DB

API -> API: Génère alertes dynamiques\n(id: "maintenance-X", "overdue-Y", etc.)

API --> UI: 200 OK\n{alerts[]}
UI -> UI: Affiche 5 premières alertes
UI -> UI: Auto-refresh après 30s

UI --> User: Affiche alertes avec icônes

deactivate API
deactivate UI

note right of API
  Alertes 100% dynamiques
  Basées sur données temps réel
  Pas de stockage en DB
end note

@enduml
```

---

### Figure 5.4: Diagramme d'Activité "Suivre Maintenance"

**Nom fichier:** `figure_5_4_activite_maintenance.png`

```plantuml
@startuml
start

:Technicien consulte\nles maintenances assignées;

if (Maintenance disponible?) then (oui)
  :Sélectionne maintenance;
  :Consulte détails actif;
  
  :Change statut\n"en_cours";
  
  :Effectue la maintenance;
  
  if (Maintenance terminée?) then (oui)
    :Change statut\n"terminé";
    :Saisit coût;
    :Ajoute notes;
    :Renseigne date completion;
    
    :Système met à jour\nstatut actif;
    
    note right
      L'alerte dynamique
      disparaîtra automatiquement
    end note
    
  else (non)
    :Maintenance reste\n"en_cours";
  endif
  
else (non)
  :Aucune maintenance\nà traiter;
endif

stop

@enduml
```

---

## 💬 SPRINT 4: MESSAGERIE

### Figure 6.1: Cas d'Utilisation Messagerie

**Nom fichier:** `figure_6_1_uc_messagerie.png`

```plantuml
@startuml
left to right direction

actor "Utilisateur" as User

rectangle "Messagerie" {
  usecase "Envoyer message" as UC1
  usecase "Créer groupe" as UC2
  usecase "Consulter conversations" as UC3
  usecase "Recevoir notifications" as UC4
  usecase "Rechercher messages" as UC5
  usecase "Ajouter emoji" as UC6
}

User --> UC1
User --> UC2
User --> UC3
User --> UC4
User --> UC5

UC1 ..> UC6 : <<extend>>

note right of UC2
  Un groupe permet
  la discussion entre
  plusieurs utilisateurs
end note

@enduml
```

---

### Figure 6.2: Diagramme de Classes Sprint 4

**Nom fichier:** `figure_6_2_classes_sprint4.png`

```plantuml
@startuml
skinparam classAttributeIconSize 0

class User {
  - id: Integer {PK}
  - full_name: String
  - email: String
}

class Message {
  - id: Integer {PK}
  - sender_id: Integer {FK}
  - receiver_id: Integer {FK}
  - group_id: Integer {FK}
  - content: String
  - timestamp: DateTime
  - is_read: Boolean
  __
  + to_dict(): dict
  + mark_as_read(): void
}

class Group {
  - id: Integer {PK}
  - name: String
  - created_by: Integer {FK}
  - created_at: DateTime
  __
  + to_dict(): dict
  + add_member(user_id): void
}

class GroupMember {
  - id: Integer {PK}
  - group_id: Integer {FK}
  - user_id: Integer {FK}
  - joined_at: DateTime
}

User "1" -- "*" Message : envoie >
User "1" -- "*" Message : reçoit >
Group "1" -- "*" Message : contient >
Group "1" -- "*" GroupMember : a >
User "1" -- "*" GroupMember : appartient à >
User "1" -- "*" Group : crée >

note right of Message
  Message 1-1:
  - receiver_id != null
  - group_id = null
  
  Message groupe:
  - receiver_id = null
  - group_id != null
end note

@enduml
```

---

### Figure 6.3: Séquence "Envoyer Message"

**Nom fichier:** `figure_6_3_seq_envoyer_message.png`

```plantuml
@startuml
actor "User1" as User1
participant "Messenger UI" as UI
participant "API Backend" as API
database "Base de Données" as DB
actor "User2" as User2

User1 -> UI: Tape message dans input
activate UI
User1 -> UI: Clique bouton "Envoyer"

UI -> API: POST /api/messages\n{receiver_id: 2, content: "..."}
activate API

API -> DB: INSERT INTO messages\n(sender_id, receiver_id, content, timestamp)
activate DB
DB --> API: Retourne message créé
deactivate DB

API --> UI: 201 Created\n{message}
UI -> UI: Ajoute message à la conversation
UI --> User1: Affiche message envoyé

alt User2 est en ligne
    UI --> User2: Notification temps réel\n"Nouveau message de User1"
end

deactivate API
deactivate UI

@enduml
```

---

### Figure 6.4: Séquence "Créer Groupe"

**Nom fichier:** `figure_6_4_seq_creer_groupe.png`

```plantuml
@startuml
actor "Admin Groupe" as Admin
participant "UI Messenger" as UI
participant "API Backend" as API
database "Base de Données" as DB

Admin -> UI: Clique "Créer Groupe"
activate UI
UI --> Admin: Affiche modal

Admin -> UI: Saisit nom groupe
Admin -> UI: Sélectionne membres\n(User2, User3, User4)
Admin -> UI: Clique "Créer"

UI -> API: POST /api/groups\n{name: "Équipe", members: [2,3,4]}
activate API

API -> DB: INSERT INTO groups\n(name, created_by)
activate DB
DB --> API: Retourne group.id
deactivate DB

loop Pour chaque membre
    API -> DB: INSERT INTO group_members\n(group_id, user_id)
    activate DB
    DB --> API: OK
    deactivate DB
end

API --> UI: 201 Created\n{group}
UI -> UI: Ajoute groupe à la liste
UI --> Admin: Affiche groupe créé\n"Groupe Équipe créé"

deactivate API
deactivate UI

note right of Admin
  Admin peut maintenant
  envoyer des messages
  au groupe
end note

@enduml
```

---

## ✅ RÉCAPITULATIF

**Total: 20 diagrammes UML créés**

### Par Sprint:
- Architecture: 2 diagrammes
- Chapitre 2: 2 diagrammes
- Sprint 1: 6 diagrammes ✅
- Sprint 2: 4 diagrammes ✅
- Sprint 3: 4 diagrammes ✅
- Sprint 4: 4 diagrammes ✅

### Instructions:
1. Copiez chaque code PlantUML
2. Générez sur http://www.plantuml.com/plantuml/uml/
3. Téléchargez PNG
4. Renommez selon le nom indiqué

**Temps estimé: 2-3 heures pour tous les diagrammes**

---

**Tous les diagrammes UML sont prêts à être générés!** 🎨
