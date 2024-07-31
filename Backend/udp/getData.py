import socket
import json
from saveData import save_data

UDP_IP = "127.0.0.1"
UDP_PORT = 8182

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT}")

def get_json_data():
    data, addr = sock.recvfrom(1024)

    data_str = data.decode('utf-8', errors='ignore')  

    json_start = data_str.find('{')
    json_end = data_str.rfind('}') + 1
    clean_json_str = data_str[json_start:json_end]

    clean_json_str = clean_json_str.replace('FALSE', 'false').replace('TRUE', 'true')

    try:
        data_json = json.loads(clean_json_str)

        save_data(data_json)
        return clean_json_str

    except (json.JSONDecodeError, KeyError) as e:
        return "{}"

if __name__ == "__main__":
    while True:
        get_json_data()
