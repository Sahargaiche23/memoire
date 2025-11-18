FROM node:18-alpine as builder

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Builder l'application
RUN npm run build

# Stage de production
FROM node:18-alpine

WORKDIR /app

# Installer serve pour servir l'application
RUN npm install -g serve

# Copier les fichiers buildés depuis le stage builder
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

# Exposer le port
EXPOSE 3000

# Commande de démarrage
CMD ["serve", "-s", "build", "-l", "3000"]
