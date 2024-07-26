from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

token = ""
org = ""
url = ""
bucket = ""

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()