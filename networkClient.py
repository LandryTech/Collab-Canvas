import socket

class NetworkClient:
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
    
    # Returns the IP
    def getIP(self):
        return self.ip
    
    # Returns the Port
    def getPort(self):
        return self.port
    
    def send(self, msg):
        if (isinstance(msg, list)): # Combines into one string separated by '<'
            msg = "<".join(msg)

        if (not isinstance(msg, bytes)): # Encodes the message if not already
            msg = msg.encode()

        self.client_socket.sendall(msg)
    
    def receive(self):
        return self.client_socket.recv(1024).decode().split('<') # Decodes message and splits for '<'