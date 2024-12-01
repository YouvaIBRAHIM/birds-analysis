import os

os.environ['HADOOP_CONF_DIR'] = '/opt/hadoop/etc/hadoop'  # Chemin vers les fichiers de configuration Hadoop
os.environ['YARN_CONF_DIR'] = '/opt/hadoop/etc/hadoop'  # Chemin vers les fichiers de configuration YARN
os.environ['SPARK_HOME'] = '/opt/spark' 
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-1.11.0-openjdk-amd64'
import findspark
findspark.init('/opt/spark')

from pyspark.sql import SparkSession

spark = SparkSession.builder.enableHiveSupport().getOrCreate()

# spark.sql("CREATE TABLE IF NOT EXISTS src (key INT, value STRING) USING hive")
# spark.sql("LOAD DATA LOCAL INPATH '/opt/spark/examples/src/main/resources/kv1.txt' INTO TABLE src")


# spark.sql("SELECT * FROM src").show()
