import grpc
import os
import time
import monitor_pb2
import monitor_pb2_grpc

def admin():
    server_address = "localhost:35491"

    with grpc.insecure_channel(server_address) as channel:
        stub = monitor_pb2_grpc.MetricServiceStub(channel)

        try:
            stream = stub.WatchAllDevices(monitor_pb2.AdminRequest())

            for response in stream:
                os.system('cls' if os.name == 'nt' else 'clear')

                # Esta seção de impressão foi feita com o uso de IA
                print("====================================================================")
                print("           HARDWARE MONITOR SYSTEM DASHBOARD (gRPC)      ")
                print("====================================================================")
                print(f"{'MACHINE':<20} | {'CPU':<8} | {'MEMORY':<8} | {'DISK':<8} | {'LAST UPDATE'}")
                print("--------------------------------------------------------------------")

                if not response.devices:
                    print("There is no machines sending metrics")

                for device in response.devices:
                    print(f"{device.client_id:<20} | {device.cpu:>5.1f}% | {device.memory:>7.1f}% | {device.disk:>5.1f}% | {device.last_update}")
                    print("====================================================================")
            print("Ctrl+C to stop application.")

        except KeyboardInterrupt:
            print("Panel closed")
        except grpc.RpcError as e:
            print(f"gRPC err: {e}")

if __name__ == '__main__':
    admin()

