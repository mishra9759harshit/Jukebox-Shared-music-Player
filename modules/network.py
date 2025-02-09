import socket
import threading

class Network:
    def __init__(self, port=5000, host="0.0.0.0"):
        self.host = host  # Local host
        self.port = port  # Port for communication
        self.server_socket = None  # Server socket
        self.client_socket = None  # Client socket
        self.connections = []  # List of connected clients

    def start_server(self):
        """Start the server to listen for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Allow up to 5 clients
        print(f"Server started, waiting for connections on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        """Handle incoming data from clients."""
        while True:
            try:
                data = conn.recv(1024).decode()
                if data:
                    print(f"Received from {addr}: {data}")
                    self.broadcast(data)
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                self.connections.remove(conn)
                conn.close()
                break

    def broadcast(self, message):
        """Send a message to all connected clients."""
        for conn in self.connections:
            try:
                conn.send(message.encode())
            except:
                self.connections.remove(conn)

    def connect_to_server(self, ip):
        """Connect to a server as a client."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((ip, self.port))
            print(f"Connected to server at {ip}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message):
        """Send a message to the connected server."""
        if self.client_socket:
            self.client_socket.send(message.encode())

    def close_connection(self):
        """Close the client or server connection."""
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()

