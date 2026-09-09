import socket
import logging
import threading

PORT = 35491

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("monitor.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def client(client_socket, client_address):
    logging.info(f"Connection accepted from {client_address}")
    while True:
        try:
            # recv is blocking and it defines the max size of the buffer
            clientMsg = client_socket.recv(1024)
            if not clientMsg:
                break
            
            logging.info(f"[{client_address}]      Metrics received: {clientMsg.decode()}")

            msg = "Metrics successfully processed"
            client_socket.send(msg.encode())
        except Exception as e:
            logging.error(f"Failed to communicate with {client_address}: {e}")
            break
    client_socket.close()
    logging.warning(f"Connection closed wih {client_address}")


if __name__ == '__main__':
    addr = ("0.0.0.0", PORT)
# Using IPv4 and the TCP as standard 
    s = socket.create_server(addr, family=socket.AF_INET)
    s.listen()
    logging.info("Server is up and listening")

    while True:
        try:
            # accept is blocking
            client_socket, client_address = s.accept()

            client_thread = threading.Thread(
                target = client,
                args = (client_socket, client_address),
                name = f"Client-{client_address[1]}"
            )

            client_thread.darmon = True

            client_thread.start()

        except Exception as e:
            logging.error(f"Server err: {e}")
            break

    s.close()

