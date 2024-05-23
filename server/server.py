import socket
from server.client_handler import ClientHandler
import signal
import sys
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        print("Server started and listening on port", self.port)

        def signal_handler(sig, frame):
            print("\nServer shutting down...")
            self.server_socket.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print("Connection established with", client_address)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except Exception as e:
            print("\nServer error: ", e)

    def handle_client(self, client_socket, client_address):
        try:
            client_handler = ClientHandler(client_socket)
            client_handler.login()
            client_handler.get_wallet()
            client_handler.get_password()
            client_handler.authenticate_user()
            client_handler.decision()
        except Exception as e:
            print(f"{client_address} disconnected")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = Server('0.0.0.0', 12345)
    server.start()