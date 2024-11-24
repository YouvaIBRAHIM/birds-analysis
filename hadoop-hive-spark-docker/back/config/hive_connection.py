from pyhive import hive

def get_hive_connection():
    conn = hive.Connection(host="master", port=10000, username="hive")
    return conn
