import socket
import json
import datetime
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB bağlantısı
token = ""
org = ""
url = ""
bucket = ""

# InfluxDB client oluşturma
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Veri kaydetme fonksiyonu
def save_data(data_dict):
    point = Point("sensor_data").tag("location", "office")
    for key, value in data_dict.items():
        point.field(key, value)
    point.time(datetime.datetime.utcnow(), WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
    print(f"Data saved to InfluxDB: {data_dict}")


