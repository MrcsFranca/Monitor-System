import socket
import psutil
import time
import json

IP = "192.168.18.4"
PORT = 35491

def metrics():
    return {
        "cpu": psutil.cpu_percent(interval=1, percpu=False),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }


obj = socket.socket(family=socket.AF_INET)

obj.connect((IP, PORT))
print("Connected to the server")

c = 0
while True:
    c += 1
    data = metrics()
    data = json.dumps(data).encode('utf-8')
    obj.sendall(data)

    data = obj.recv(1024)
    print(f"Server responded: {data.decode()}")

    time.sleep(2)
    if c == 5:
        break
        obj.close()

