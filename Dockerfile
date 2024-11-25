FROM python:3.9

# Ajouter les clés GPG nécessaires pour Ubuntu focal
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32 871920D1991BC93C

# Créer /etc/apt/sources.list si manquant
RUN if [ ! -f /etc/apt/sources.list ]; then \
        echo "deb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse" > /etc/apt/sources.list; \
        echo "deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse" >> /etc/apt/sources.list; \
        echo "deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse" >> /etc/apt/sources.list; \
        echo "deb http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse" >> /etc/apt/sources.list; \
    fi

# Mettre à jour et installer les dépendances nécessaires
RUN apt-get -qq update \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq install --no-install-recommends \
      openjdk-8-jdk \
    && rm -rf /var/lib/apt/lists/*

# Définir JAVA_HOME et ajouter Java au PATH
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
ENV PATH=$JAVA_HOME/bin:$PATH

# Créer et activer un environnement virtuel
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Configurer le répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY ./back/requirements.txt /app/requirements.txt

# Installer les dépendances dans l'environnement virtuel
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copier le code de l'application
COPY ./back /app

# Commande de démarrage
CMD ["fastapi", "run", "main.py", "--port", "8000", "--reload"]
