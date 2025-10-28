import socket

class NetworkServer:
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
    
    # Returns the IP
    def getIP(self):
        return self.ip
    
    # Returns the Port
    def getPort(self):
        return self.port