import socket
import logging
import threading
from concurrent import futures
import grpc
import monitor_pb2
import monitor_pb2_grpc

PORT = 35491

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("monitor.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

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

                yield monitor_pb2.MetricResponse(message="All metrics successfully processed via gRPC stream")

        except Exception as e:
            logging.error(f"Failed to communicate with client {client_address}: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return monitor_pb2.MetricResponse()

def serve():
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
