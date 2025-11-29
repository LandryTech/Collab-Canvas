import socket

class NetworkClient:
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.ip == "":
            self.ip = self.client_socket.getsockname()[0]

        self.client_socket.connect((self.ip, self.port))

    def send(self, msg):
        endChar = "<"
        endChar = endChar.encode()

        if isinstance(msg, list):
            msg = "<".join(msg)
        if not isinstance(msg, bytes):
            msg = msg.encode()
        
        self.client_socket.sendall(msg + endChar)

    def receive(self):
        data = self.client_socket.recv(1024)
        if not data:
            print("Server closed connection.")
            return None
        decoded = data.decode().split('<')
        return decoded

    def stop(self):
        self.client_socket.close()
