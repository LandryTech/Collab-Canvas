""" PURPOSE
—NETWORK SERVER—
A class for the collabServer program that starts a server for WhiteboardUI.
It retrieves messages from clients and broadcasts them to all other clients.
"""

import socket
import threading

class NetworkServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")

        self.clients = []  # List of all connected client sockets
        self.lock = threading.Lock()  # Prevents conflicts when editing the list, where no two clients can edit the list at once

    # Takes a client message and sends it to all other clients
    def broadcast(self, msg, sender_socket=None):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:  # Don’t send back to sender
                    try:
                        client.sendall(msg)
                    except:
                        # If a client is disconnected, remove it
                        self.clients.remove(client)

    # Receives and sends client data
    def handle_client(self, client_socket, addr):
        print(f"New connection from {addr}")
        with self.lock:
            self.clients.append(client_socket)

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break  # client disconnected

                decoded = data.decode()
                print(f"Received from {addr}: {decoded}")

                # Broadcast to all other clients
                self.broadcast(f"{decoded}".encode(), sender_socket=client_socket)

            except ConnectionResetError:
                print(f"Connection lost from {addr}")
                break

        with self.lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
        client_socket.close()
        print(f"Connection closed for {addr}")

    # Searches for and accepts client connections
    def start(self):
        print("Waiting for clients...")
        while True:
            client_socket, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()

""" REFERENCES
—THREADING—
The server uses threading to process receiving point data from multiple clients at a time.
Without threading, the server needs to receive messages from every client before being able
to broadcast messages back to the clients.
[1] https://www.geeksforgeeks.org/python/multithreading-python-set-1/
[2] https://www.geeksforgeeks.org/python/socket-programming-multi-threading-python/
"""