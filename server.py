import socket
import logging
import threading
from concurrent import futures
import grpc
import monitor_pb2
import monitor_pb2_grpc
import time
import datetime

PORT = 35491

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("monitor.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

shared_cluster_status = {}

class MetricServiceServicer(monitor_pb2_grpc.MetricServiceServicer):
    # preciso passar um iterador pq a classe foi criada com o stream
    def StreamMetrics(self, request_iterator, context):
        client_address = context.peer()
        logging.info(f"Connection accepted from gRPC client: {client_address}")

        try:
            for request in request_iterator:
                logging.info(
                    f"[{request.client_id}] Metrics received -> "
                    f"CPU: {request.cpu:.1f}%, "
                    f"Memory: {request.memory:.1f}%, "
                    f"Disk: {request.disk:.1f}%"
                )

                shared_cluster_status[request.client_id] = {
                    "cpu": request.cpu,
                    "memory": request.memory,
                    "disk": request.disk,
                    "time": datetime.datetime.now().strftime("%H:%M:%S")
                }

            return monitor_pb2.MetricResponse(message="All metrics successfully processed via gRPC stream")

        except Exception as e:
            logging.error(f"Failed to communicate with client {client_address}: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return monitor_pb2.MetricResponse()

    def WatchAllDevices(self, request, context):
        # o context, aqui, serve para pegar dados da conexão
        admin_address = context.peer()
        logging.info(f"New Admin dashboard connected from: {admin_address}")
        
        try:
            while context.is_active():
                device_list = []

                for client_id, data in shared_cluster_status.items():
                    device = monitor_pb2.DeviceStatus(
                        client_id=client_id,
                        cpu=data["cpu"],
                        memory=data["memory"],
                        disk=data["disk"],
                        last_update=data["time"]
                    )
                    device_list.append(device)

                # o yield é um gerador, então quanto a resposta é devolvida para que chamou a função, quando a função for chamada novamente, ela retorna de onde parou
                yield monitor_pb2.SystemStatusResponse(devices=device_list)
                time.sleep(1)

        except Exception as e:
            logging.error(f"Admin connection error with {admin_address}: {e}")
        finally:
            # acontece independente do try ou except
            logging.info(f"Admin dashboard disconnected: {admin_address}")

def serve():
    # o futures serve para criar uma pool de threads para trabalharem juntas, indico a quantidade de threads que podem ser usadas
    # isso implementa a concorrência, sem isso se o cliente usasse muito o stream de métricas o servidor ficaria bloqueado
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    monitor_pb2_grpc.add_MetricServiceServicer_to_server(MetricServiceServicer(), server)
    # adiciona a porta como sendo passíel de escuta
    server.add_insecure_port(f"0.0.0.0:{PORT}")

    logging.info(f"gRPC server is up and listening on port {PORT}")
    # inicia o servidor gRPC
    server.start()

    # mantem o processo do servidor rodando enquanto ele não é explicitamente terminado
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
