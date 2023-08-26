#!/usr/bin/python3


import json
import socket
import concurrent.futures

def search_key_value_pairs(json_data):
    results = []
    for entry in json_data:
        if "protocols" in entry and "ip" in entry and "port" in entry:
            protocol = entry["protocols"]
            ip = entry["ip"]
            port = entry["port"]
            results.append({"protocol": protocol, "ip": ip, "port": port})
    return results

def check_status(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)  # Set a timeout for the connection attempt
            sock.connect((ip, int(port)))
            return "Up"
    except (socket.timeout, ConnectionRefusedError):
        return "Down"

def main():
    json_file_path = "/path/to/file.json"  # Replace with your JSON file path

    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    key_value_pairs = search_key_value_pairs(json_data)

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for entry in key_value_pairs:
            ip = entry["ip"]
            port = entry["port"]
            results.append(executor.submit(check_status, ip, port))
    for entry, result in zip(key_value_pairs, results):
        status = result.result()
        if status == "Up":
            print(f"IP: {entry['ip']}, Port: {entry['port']}, Status: {status}")
        
        

if __name__ == "__main__":
    main()
