import socket # to usando so para pegar o nome da máquina 
import psutil
import time
import json
import argparse
import grpc
import monitor_pb2
import monitor_pb2_grpc

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

def generate_metrics(client_id):
    while True:
        cpu = psutil.cpu_percent(interval=1, percpu=False)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        request = monitor_pb2.MetricRequest(client_id=client_id, cpu=cpu, memory=memory, disk=disk)

        yield request

        time.sleep(1)

if __name__ == '__main__':
    args = get_args()
    IP = args.ip
    PORT = args.port
    CLIENT_ID = socket.gethostname()

    print(f"Connecting to gRPC server at {IP}:{PORT}...")

    with grpc.insecure_channel(f"{IP}:{PORT}") as channel:
        # o insecure_channel estabelece uma comunicação de longa duração
        stub = monitor_pb2_grpc.MetricServiceStub(channel)

        try:
            responses = stub.StreamMetrics(generate_metrics(CLIENT_ID))
            # como a resposta é um fluxo stream, preciso colocar em um loop
            for response in responses:
                print(f"Server: {response.message}")
        except grpc.RpcError as e:
            print(f"gRPC error encountered: {e.details()} (Code: {e.code()})")
        except Exception as e:
            print(f"Client err: {e}")

