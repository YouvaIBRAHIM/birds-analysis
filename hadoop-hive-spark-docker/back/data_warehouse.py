import os
import csv
from pyhive import hive
import happybase
from elasticsearch import Elasticsearch

# Configuration des chemins et connexions
CSV_DIRECTORY = "/storm_events/"
HIVE_HOST = '172.28.1.2'
HBASE_HOST = '172.28.1.2'
ELASTICSEARCH_HOST = "http://elasticsearch:9200"

# Initialisation des connexions
hive_conn = hive.Connection(host=HIVE_HOST)
hbase_conn = happybase.Connection(HBASE_HOST)
es = Elasticsearch(ELASTICSEARCH_HOST)

# Création des tables dans Hive et HBase
def setup_hive_hbase():
    # Créer la table Hive
    cursor = hive_conn.cursor()
    cursor.execute("""
        CREATE EXTERNAL TABLE IF NOT EXISTS storm_events (
            start_time STRING,
            end_time STRING,
            event_type STRING,
            state STRING,
            county STRING,
            injuries INT,
            deaths INT
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        LOCATION '/storm_events/';
    """)
    print("Table Hive créée.")

    # Créer la table HBase
    hbase_conn.create_table(
        'storm_events',
        {
            'details': dict(),
            'stats': dict()
        }
    )
    print("Table HBase créée.")

# Importer les fichiers CSV dans Hive et HBase
def import_to_hive_hbase():
    table = hbase_conn.table('storm_events')

    for filename in os.listdir(CSV_DIRECTORY):
        if filename.endswith(".csv"):
            filepath = os.path.join(CSV_DIRECTORY, filename)
            print(f"Traitement du fichier : {filepath}")

            with open(filepath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Stockage dans Hive
                    cursor = hive_conn.cursor()
                    cursor.execute(f"""
                        INSERT INTO TABLE storm_events VALUES (
                            '{row['start_time']}', '{row['end_time']}', '{row['event_type']}',
                            '{row['state']}', '{row['county']}', {row['injuries']}, {row['deaths']}
                        );
                    """)

                    # Stockage dans HBase
                    table.put(
                        row['start_time'],  # Clé primaire basée sur start_time
                        {
                            'details:event_type': row['event_type'],
                            'details:state': row['state'],
                            'details:county': row['county'],
                            'stats:injuries': row['injuries'],
                            'stats:deaths': row['deaths'],
                        }
                    )

    print("Données importées dans Hive et HBase.")

# Indexer dans Elasticsearch
def index_to_elasticsearch():
    cursor = hive_conn.cursor()
    cursor.execute("SELECT * FROM storm_events")

    for row in cursor.fetchall():
        doc = {
            "start_time": row[0],
            "end_time": row[1],
            "event_type": row[2],
            "state": row[3],
            "county": row[4],
            "injuries": row[5],
            "deaths": row[6],
        }
        es.index(index="storm-events", id=row[0], body=doc)

    print("Données indexées dans Elasticsearch.")

# Workflow principal
def main():
    setup_hive_hbase()
    import_to_hive_hbase()
    index_to_elasticsearch()

if __name__ == "__main__":
    main()
