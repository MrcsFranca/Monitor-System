import socket

addr = ("0.0.0.0", 35491)
s = socket.create_server(addr, family=socket.AF_INET)

s.listen()
print("servidor funcionando")
while True:
    serverOn = s.accept()
    print("conexão aceita", serverOn[1])
    msg = "Hello World"
    clientMsg = serverOn[0].recv(1024)
    print(f"Mensagem recebida: {clientMsg.decode()}")
    serverOn[0].send(msg.encode())
    serverOn[0].close()
