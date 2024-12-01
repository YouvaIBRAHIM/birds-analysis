FROM python:3.9

# Créer et activer un environnement virtuel
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Configurer le répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY ./back/requirements.txt /app/requirements.txt

# Installer les dépendances dans l'environnement virtuel
RUN pip install -r /app/requirements.txt

# Copier le code de l'application
COPY ./back /app

# Commande de démarrage
CMD ["fastapi", "run", "main.py", "--port", "8000", "--reload"]
