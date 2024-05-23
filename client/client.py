import socket
import signal
import sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            def signal_handler(sig, frame):
                print("\nClient shutting down...")
                client_socket.close()
                sys.exit(0)

            signal.signal(signal.SIGINT, signal_handler)
            
            try:
                while True:
                    prompt = client_socket.recv(10240).decode()
                    if not prompt:
                        break
                    print(prompt)
                    data = input()
                    client_socket.sendall(data.encode())
            except socket.error:
                print("Server closed the connection.")

if __name__ == "__main__":
    client = Client('localhost', 12345)
    client.start()
