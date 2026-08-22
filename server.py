import socket
import logging

PORT = 35491

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("monitor.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

addr = ("0.0.0.0", PORT)
# Using IPv4 and the TCP as standard 
s = socket.create_server(addr, family=socket.AF_INET)
s.listen()
logging.info("Server is up and listening")

while True:
    try:
        # accept is blocking
        serverOn = s.accept()
        logging.info(f"Connection accepted from {serverOn[1]}")

        while True:
            try:
                # recv is blocking and it defines the max size of the buffer
                clientMsg = serverOn[0].recv(1024)
                if not clientMsg:
                    break
                
                logging.info(f"[{serverOn[1]}]      Metrics received: {clientMsg.decode()}")

                msg = "Metrics successfully processed"
                serverOn[0].send(msg.encode())
            except Exception as e:
                logging.error(f"Failed to communicate with {serverOn[1]}: {e}")
                break

        serverOn[0].close()
        logging.warning(f"Connection closed with {serverOn[1]}. Waiting for a new connection")

    except Exception as e:
        print(f"Server err: {e}")
        serverOn[0].close()
        break

