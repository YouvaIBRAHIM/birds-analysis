FROM hadoop-hive-spark-base AS base

FROM tensorflow/tensorflow:latest-jupyter

FROM python:3.9

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Ajouter les clés GPG nécessaires pour Ubuntu focal
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32 871920D1991BC93C

# Créer /etc/apt/sources.list si manquant
RUN if [ ! -f /etc/apt/sources.list ]; then \
        echo "deb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse" > /etc/apt/sources.list; \
        echo "deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse" >> /etc/apt/sources.list; \
        echo "deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse" >> /etc/apt/sources.list; \
        echo "deb http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse" >> /etc/apt/sources.list; \
    fi

# Mise à jour des paquets et installation des dépendances nécessaires
RUN apt-get -qq update  \
 && DEBIAN_FRONTEND=noninteractive apt-get -qq install --no-install-recommends \
      sudo \
      openjdk-8-jdk \
      curl \
      coreutils \
      libc6-dev \
 && rm -rf /var/lib/apt/lists/*

# Définir l'utilisateur et le groupe
ARG USERNAME=jupyter
ARG GROUPNAME=jupyter
ARG UID=1001
ARG GID=1001

RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
 && chmod 0440 /etc/sudoers.d/$USERNAME \
 && groupadd -g $GID $GROUPNAME \
 && useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

USER $USERNAME

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

# Hadoop
COPY --from=base --chown=$USERNAME:$GROUPNAME /opt/hadoop /opt/hadoop
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH

# Spark
COPY --from=base --chown=$USERNAME:$GROUPNAME /opt/spark /opt/spark
ENV SPARK_HOME=/opt/spark
ENV PYTHONHASHSEED=1
ENV PYSPARK_PYTHON=python3
ENV SPARK_CONF_DIR=$SPARK_HOME/conf
ENV PATH=$SPARK_HOME/sbin:$SPARK_HOME/bin:$PATH

# Hive
COPY --from=base --chown=$USERNAME:$GROUPNAME /opt/hive /opt/hive
ENV HIVE_HOME=/opt/hive
ENV HIVE_CONF_DIR=$HIVE_HOME/conf
ENV PATH=$HIVE_HOME/sbin:$HIVE_HOME/bin:$PATH

WORKDIR /home/$USERNAME

COPY . /home/$USERNAME/

RUN sudo pip install -r /home/$USERNAME/requirements.txt

RUN sudo chmod a+x /home/$USERNAME/run.sh
CMD ["sudo", "fastapi", "run", "main.py", "--port", "8000", "--reload"]
