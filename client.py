import socket

obj = socket.socket(family=socket.AF_INET)

obj.connect(("172.31.67.237", 35491))
print("conectado ao servidor")

msg = "olá"
bytes_msg = str.encode(msg)
obj.sendall(bytes_msg)
data = obj.recv(1024)
print(f"O servidor disse: {data.decode()}")
obj.close()

