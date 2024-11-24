FROM hadoop-hive-spark-base

ENV DATADIR=/opt/hadoop/dfs/data
RUN mkdir -p /opt/hadoop/dfs/data
VOLUME /opt/hadoop/dfs/data

ENV SPARK_PUBLIC_DNS=localhost
ENV SPARK_MASTER_ADDRESS=spark://master:7077

RUN sudo chmod -R 700 /opt/hadoop/dfs/data
RUN sudo chown -R jupyter:jupyter /opt/hadoop/dfs/data

COPY run.sh /usr/local/sbin/run.sh
RUN sudo chmod a+x /usr/local/sbin/run.sh
CMD ["run.sh"]