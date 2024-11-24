from app.v1.scripts.load.storm_events import load_storm_events_to_hadoop
from app.v1.scripts.load.gsod import load_gsod_to_hadoop
from hdfs import InsecureClient

hdfs_client = InsecureClient('http://master:9870', user='jupyter')

load_storm_events_to_hadoop(hdfs_client)
load_gsod_to_hadoop(hdfs_client)