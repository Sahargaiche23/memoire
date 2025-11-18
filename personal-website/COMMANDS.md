# 🔧 Commandes Utiles

## Backend

### Installation et Configuration

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python init_db.py

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Mettre à jour les dépendances
pip install -r requirements.txt --upgrade
```

### Exécution

```bash
# Démarrer le serveur de développement
python app.py

# Démarrer avec Gunicorn (production)
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

# Démarrer sur un port différent
python app.py --port 5001
```

### Gestion de la Base de Données

```bash
# Réinitialiser la base de données
rm patrimoine.db
python init_db.py

# Sauvegarder la base de données
cp patrimoine.db patrimoine_backup_$(date +%Y%m%d).db

# Restaurer une sauvegarde
cp patrimoine_backup_YYYYMMDD.db patrimoine.db
```

### Dépannage

```bash
# Vérifier que Python est installé
python --version

# Vérifier les dépendances installées
pip list

# Vérifier que le serveur répond
curl http://localhost:5000/api/statistics

# Voir les logs en temps réel
tail -f app.log
```

---

## Frontend

### Installation et Configuration

```bash
# Installer les dépendances
npm install

# Installer une dépendance spécifique
npm install <package-name>

# Mettre à jour les dépendances
npm update

# Nettoyer le cache npm
npm cache clean --force

# Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install
```

### Exécution

```bash
# Démarrer le serveur de développement
npm start

# Compiler l'application pour la production
npm run build

# Servir la version compilée localement
npm install -g serve
serve -s build -l 3000

# Démarrer sur un port différent
PORT=3001 npm start
```

### Dépannage

```bash
# Vérifier que Node.js est installé
node --version
npm --version

# Vérifier les dépendances
npm list

# Vérifier les problèmes
npm audit

# Corriger les problèmes automatiquement
npm audit fix

# Nettoyer les fichiers temporaires
rm -rf build node_modules
npm install
npm run build
```

---

## Docker

### Commandes de Base

```bash
# Construire les images
docker-compose build

# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir le statut des services
docker-compose ps

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Gestion des Conteneurs

```bash
# Redémarrer un service
docker-compose restart backend

# Reconstruire un service
docker-compose up -d --build backend

# Exécuter une commande dans un conteneur
docker-compose exec backend python init_db.py

# Accéder au shell d'un conteneur
docker-compose exec backend sh
docker-compose exec frontend sh
```

### Nettoyage

```bash
# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer les volumes (données)
docker-compose down -v

# Supprimer les images
docker rmi patrimoine-municipal_backend patrimoine-municipal_frontend

# Nettoyer complètement
docker system prune -a
```

---

## Base de Données

### PostgreSQL (Production)

```bash
# Se connecter à PostgreSQL
psql -U patrimoine_user -d patrimoine_db

# Créer une sauvegarde
pg_dump -U patrimoine_user patrimoine_db > backup.sql

# Restaurer une sauvegarde
psql -U patrimoine_user patrimoine_db < backup.sql

# Compresser une sauvegarde
gzip backup.sql

# Restaurer une sauvegarde compressée
gunzip < backup.sql.gz | psql -U patrimoine_user patrimoine_db
```

### SQLite (Développement)

```bash
# Ouvrir la base de données
sqlite3 patrimoine.db

# Voir les tables
.tables

# Voir le schéma d'une table
.schema assets

# Exporter en CSV
.mode csv
.output assets.csv
SELECT * FROM assets;
.output stdout

# Quitter
.quit
```

---

## Git

### Configuration

```bash
# Initialiser un repository
git init

# Cloner un repository
git clone <url>

# Configurer l'utilisateur
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"
```

### Commandes Courantes

```bash
# Voir le statut
git status

# Ajouter des fichiers
git add .
git add <fichier>

# Commiter les changements
git commit -m "Message du commit"

# Voir l'historique
git log
git log --oneline

# Voir les différences
git diff
git diff <fichier>

# Pousser vers le serveur
git push origin main

# Récupérer les changements
git pull origin main

# Créer une branche
git checkout -b <nom-branche>

# Changer de branche
git checkout <nom-branche>

# Fusionner une branche
git merge <nom-branche>

# Supprimer une branche
git branch -d <nom-branche>
```

---

## Nginx

### Commandes

```bash
# Tester la configuration
sudo nginx -t

# Démarrer Nginx
sudo systemctl start nginx

# Arrêter Nginx
sudo systemctl stop nginx

# Redémarrer Nginx
sudo systemctl restart nginx

# Recharger la configuration
sudo systemctl reload nginx

# Voir le statut
sudo systemctl status nginx

# Voir les logs d'erreur
sudo tail -f /var/log/nginx/error.log

# Voir les logs d'accès
sudo tail -f /var/log/nginx/access.log
```

---

## Systemd (Services Linux)

### Commandes

```bash
# Démarrer un service
sudo systemctl start patrimoine-backend

# Arrêter un service
sudo systemctl stop patrimoine-backend

# Redémarrer un service
sudo systemctl restart patrimoine-backend

# Voir le statut
sudo systemctl status patrimoine-backend

# Activer au démarrage
sudo systemctl enable patrimoine-backend

# Désactiver au démarrage
sudo systemctl disable patrimoine-backend

# Voir les logs
sudo journalctl -u patrimoine-backend -f

# Voir les 50 dernières lignes
sudo journalctl -u patrimoine-backend -n 50
```

---

## Certificats SSL

### Let's Encrypt

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot certonly --nginx -d your-domain.com

# Renouveler les certificats
sudo certbot renew

# Tester le renouvellement automatique
sudo certbot renew --dry-run

# Voir les certificats
sudo certbot certificates

# Supprimer un certificat
sudo certbot delete --cert-name your-domain.com
```

---

## Monitoring

### Ressources Système

```bash
# Voir l'utilisation CPU et mémoire
top

# Voir l'utilisation disque
df -h

# Voir l'utilisation mémoire
free -h

# Voir les processus
ps aux

# Voir les ports ouverts
netstat -tuln
sudo lsof -i :5000
```

### Logs

```bash
# Voir les logs système
sudo journalctl -f

# Voir les logs d'une application
sudo journalctl -u patrimoine-backend -f

# Voir les logs Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Voir les logs d'une date spécifique
sudo journalctl --since "2024-11-13 10:00:00"
```

---

## Utilitaires

### Curl (Tests API)

```bash
# GET
curl http://localhost:5000/api/statistics

# POST
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# PUT
curl -X PUT http://localhost:5000/api/assets/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Nouvel actif"}'

# DELETE
curl -X DELETE http://localhost:5000/api/assets/1 \
  -H "Authorization: Bearer <token>"
```

### Wget (Téléchargement)

```bash
# Télécharger un fichier
wget https://example.com/file.zip

# Télécharger avec un nom différent
wget -O newname.zip https://example.com/file.zip

# Télécharger récursivement
wget -r https://example.com
```

---

## Déploiement

### Build et Déploiement

```bash
# Build le frontend
cd frontend
npm run build

# Déployer sur Netlify
netlify deploy --prod --dir=build

# Déployer sur Heroku
heroku login
git push heroku main

# Déployer sur AWS
aws s3 sync build/ s3://mon-bucket/
```

---

## Sauvegarde et Restauration

### Sauvegarde Complète

```bash
# Créer une sauvegarde complète
tar -czf patrimoine_backup_$(date +%Y%m%d).tar.gz \
  backend/ frontend/ docker-compose.yml

# Restaurer une sauvegarde
tar -xzf patrimoine_backup_YYYYMMDD.tar.gz
```

### Sauvegarde Sélective

```bash
# Sauvegarder la base de données
pg_dump -U patrimoine_user patrimoine_db | gzip > db_backup.sql.gz

# Sauvegarder les fichiers de configuration
tar -czf config_backup.tar.gz backend/.env frontend/.env
```

---

## Dépannage Rapide

### Problèmes Courants

```bash
# Port déjà utilisé
lsof -i :5000
kill -9 <PID>

# Permissions refusées
sudo chown -R $USER:$USER .

# Espace disque insuffisant
df -h
du -sh *

# Connexion refusée
telnet localhost 5000
curl -v http://localhost:5000

# Erreur de dépendances
pip install --upgrade pip
npm cache clean --force
```

---

## Raccourcis Utiles

### Alias Bash

```bash
# Ajouter à ~/.bashrc ou ~/.zshrc

# Backend
alias backend-start='cd backend && source venv/bin/activate && python app.py'
alias backend-init='cd backend && python init_db.py'

# Frontend
alias frontend-start='cd frontend && npm start'
alias frontend-build='cd frontend && npm run build'

# Docker
alias docker-start='docker-compose up -d'
alias docker-stop='docker-compose down'
alias docker-logs='docker-compose logs -f'

# Git
alias gst='git status'
alias gad='git add .'
alias gcm='git commit -m'
alias gps='git push'
alias gpl='git pull'
```

---

**Dernière mise à jour**: Novembre 2024
