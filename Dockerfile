FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier seulement requirements.txt pour profiter du cache Docker
COPY requirements.txt .

# Mettre à jour pip et installer les dépendances
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Exposer le port de Django
EXPOSE 8000

# Variable d'environnement pour Django
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Commande par défaut (tu peux la surcharger pour Celery)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
