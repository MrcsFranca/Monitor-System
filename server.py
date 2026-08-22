import socket

PORT = 35491

addr = ("0.0.0.0", PORT)
s = socket.create_server(addr, family=socket.AF_INET)

s.listen()
print("server is up")
serverOn = s.accept()
print("conection accepted", serverOn[1])

c = 0
while True:
    c += 1

    clientMsg = serverOn[0].recv(1024)
    print(f"Message received: {clientMsg.decode()}")

    msg = "Message succesfully sent"
    serverOn[0].send(msg.encode())

    if c == 5:
        break
        serverOn[0].close()
