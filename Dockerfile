FROM python:3.11

WORKDIR /app

# Copier seulement requirements.txt d'abord
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=backend.settings

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
