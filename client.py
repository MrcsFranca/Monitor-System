import socket
import psutil
import time
import json
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description="Use a server to monitor your client :)"
    )

    parser.add_argument(
        "--ip",
        required=True,
        help="IP address from the server"
    )

    parser.add_argument(
        "--port",
        required=True,
        help="Port from server"
    )

    return parser.parse_args()

def metrics():
    return {
        "cpu": psutil.cpu_percent(interval=1, percpu=False),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }


if __name__ == '__main__':
    args = get_args()
    IP = args.ip
    PORT = args.port
    PORT = int(PORT)

    #Using IPv4
    obj = socket.socket(family=socket.AF_INET)
    obj.connect((IP, PORT))
    print("Connected to the server")

    while True:
        try:
            data = metrics()
            data = json.dumps(data).encode('utf-8')
            obj.sendall(data)

            data = obj.recv(1024)
            print(f"Server responded: {data.decode()}")
            
            time.sleep(2)

        except Exception as e:
            print(f"Client err: {e}")
            break

