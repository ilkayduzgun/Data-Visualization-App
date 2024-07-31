import socket
import json
from collections import deque

UDP_IP = "127.0.0.1"
UDP_PORT = 8182

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT}")

data_queue = deque()

def get_json_data():
    data, addr = sock.recvfrom(1024)
    print(f"Received raw data: {data}") 

    data_str = data.decode('utf-8', errors='ignore')
    print(f"Decoded data: {data_str}")  

    json_start = data_str.find('{')
    json_end = data_str.rfind('}') + 1
    clean_json_str = data_str[json_start:json_end]

    print(f"Clean JSON data: {clean_json_str}")  
    clean_json_str = clean_json_str.replace('FALSE', 'false').replace('TRUE', 'true')

    try:
        data_json = json.loads(clean_json_str)

        for key, value in data_json.items():
            print(f"{key}: {value}")

        data_queue.append(data_json) 
        print(f"Data added to queue: {data_json}")

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing data: {e}")

def start_udp_listener():
    while True:
        get_json_data()

if __name__ == "__main__":
    start_udp_listener()
