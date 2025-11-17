# 🚀 Guide de Déploiement en Production

## Vue d'ensemble

Ce guide couvre le déploiement du système de gestion du patrimoine municipal sur un serveur de production.

---

## 📋 Prérequis

- Serveur Linux (Ubuntu 20.04 LTS recommandé)
- Accès SSH au serveur
- Domaine configuré (optionnel)
- Certificat SSL (recommandé)

---

## 🔧 Configuration du Serveur

### 1. Mise à jour du système

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3.11 python3-pip python3-venv nodejs npm nginx postgresql postgresql-contrib
```

### 2. Créer un utilisateur dédié

```bash
sudo useradd -m -s /bin/bash patrimoine
sudo usermod -aG sudo patrimoine
sudo su - patrimoine
```

### 3. Cloner le projet

```bash
git clone <votre-repo> patrimoine-municipal
cd patrimoine-municipal
```

---

## 🗄️ Configuration de la Base de Données

### Créer une base de données PostgreSQL

```bash
sudo -u postgres psql

# Dans PostgreSQL:
CREATE DATABASE patrimoine_db;
CREATE USER patrimoine_user WITH PASSWORD 'secure_password_here';
ALTER ROLE patrimoine_user SET client_encoding TO 'utf8';
ALTER ROLE patrimoine_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE patrimoine_user SET default_transaction_deferrable TO on;
ALTER ROLE patrimoine_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE patrimoine_db TO patrimoine_user;
\q
```

### Mettre à jour la configuration

```bash
# backend/.env
DATABASE_URL=postgresql://patrimoine_user:secure_password_here@localhost:5432/patrimoine_db
JWT_SECRET_KEY=your-very-secure-random-key-here-min-32-chars
FLASK_ENV=production
```

---

## 🐍 Configuration du Backend

### Installation des dépendances

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Initialiser la base de données

```bash
python init_db.py
```

### Créer un service systemd

```bash
sudo nano /etc/systemd/system/patrimoine-backend.service
```

Ajouter:
```ini
[Unit]
Description=Patrimoine Municipal Backend
After=network.target

[Service]
User=patrimoine
WorkingDirectory=/home/patrimoine/patrimoine-municipal/backend
Environment="PATH=/home/patrimoine/patrimoine-municipal/backend/venv/bin"
ExecStart=/home/patrimoine/patrimoine-municipal/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Activer le service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable patrimoine-backend
sudo systemctl start patrimoine-backend
sudo systemctl status patrimoine-backend
```

---

## ⚛️ Configuration du Frontend

### Build de production

```bash
cd frontend
npm install
npm run build
```

### Servir avec Nginx

```bash
sudo nano /etc/nginx/sites-available/patrimoine
```

Ajouter:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirection HTTP vers HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # Certificats SSL
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Configuration SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Frontend React
    location / {
        root /home/patrimoine/patrimoine-municipal/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css text/javascript application/json;
}
```

Activer le site:
```bash
sudo ln -s /etc/nginx/sites-available/patrimoine /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔐 SSL avec Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

Renouvellement automatique:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 📊 Monitoring et Logs

### Logs du Backend

```bash
sudo journalctl -u patrimoine-backend -f
```

### Logs de Nginx

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Monitoring des ressources

```bash
# Installer Prometheus et Grafana (optionnel)
sudo apt-get install prometheus grafana-server
```

---

## 🔄 Sauvegarde et Restauration

### Script de sauvegarde

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/home/patrimoine/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Sauvegarder la base de données
pg_dump -U patrimoine_user patrimoine_db > $BACKUP_DIR/db_$DATE.sql

# Compresser
gzip $BACKUP_DIR/db_$DATE.sql

# Garder seulement les 7 dernières sauvegardes
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "Sauvegarde complétée: $BACKUP_DIR/db_$DATE.sql.gz"
```

Ajouter à crontab:
```bash
crontab -e
# Ajouter: 0 2 * * * /home/patrimoine/backup.sh
```

### Restauration

```bash
gunzip < /home/patrimoine/backups/db_YYYYMMDD_HHMMSS.sql.gz | psql -U patrimoine_user patrimoine_db
```

---

## 🔄 Mise à Jour

### Mettre à jour le code

```bash
cd /home/patrimoine/patrimoine-municipal
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart patrimoine-backend

# Frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart nginx
```

---

## 📈 Performance

### Optimisations recommandées

1. **Caching**
   ```nginx
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

2. **Compression**
   ```nginx
   gzip on;
   gzip_vary on;
   gzip_min_length 1024;
   gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
   ```

3. **Connection pooling**
   ```python
   # Dans app.py
   app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
       'pool_size': 10,
       'pool_recycle': 3600,
       'pool_pre_ping': True,
   }
   ```

---

## 🚨 Monitoring de Sécurité

### Fail2ban

```bash
sudo apt-get install fail2ban

sudo nano /etc/fail2ban/jail.local
```

Ajouter:
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
```

---

## ✅ Checklist de Déploiement

- [ ] Serveur Linux configuré
- [ ] PostgreSQL installé et configuré
- [ ] Backend déployé avec Gunicorn
- [ ] Frontend compilé et servi par Nginx
- [ ] SSL/TLS configuré
- [ ] Firewall configuré
- [ ] Sauvegardes automatiques en place
- [ ] Monitoring configuré
- [ ] Logs configurés
- [ ] Domaine pointant vers le serveur
- [ ] Tests de fonctionnalité complétés
- [ ] Performance testée

---

## 📞 Troubleshooting

### Backend ne démarre pas

```bash
sudo systemctl status patrimoine-backend
sudo journalctl -u patrimoine-backend -n 50
```

### Erreur de connexion à la BD

```bash
# Vérifier la connexion PostgreSQL
psql -U patrimoine_user -d patrimoine_db -h localhost
```

### Frontend ne se charge pas

```bash
# Vérifier les logs Nginx
sudo tail -f /var/log/nginx/error.log
```

---

**Déploiement en production terminé! 🎉**
