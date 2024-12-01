FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Installer Java, Python et autres outils nécessaires
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk python3 python3-pip curl libpq-dev openssh-server && \
    apt-get clean

# Créer un utilisateur et groupe non-root
ARG USERNAME=jupyter
ARG GROUPNAME=jupyter
ARG UID=1001
ARG GID=1001

# Configurer l'utilisateur jupyter
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

# Préparer les répertoires et ajuster les permissions
RUN mkdir -p /opt/spark /var/run/sshd && \
    chown -R $USERNAME:$GROUPNAME /opt/spark && \
    chmod 755 /var/run/sshd

# Installer Apache Spark sous root
ENV SPARK_VERSION=3.4.4
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark

RUN curl --retry 3 -O https://dlcdn.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    tar -xvf spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    mv spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION/* $SPARK_HOME/ && \
    rm -rf spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION

# Configurer PATH pour Spark
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"

# Copier les fichiers d'application
WORKDIR /app
COPY . /app/

# Installer les dépendances Python
RUN pip3 install -r /app/requirements.txt

# Donner les droits nécessaires à l'utilisateur jupyter
RUN chown -R $USERNAME:$GROUPNAME /app /opt/spark

# Copier le script d'initialisation
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# # Passer à l'utilisateur non-root pour exécuter l'application
# USER $USERNAME

# Exposer les ports nécessaires
EXPOSE 7077 8080 8000

# Lancer le script d'initialisation
CMD ["/entrypoint.sh"]
