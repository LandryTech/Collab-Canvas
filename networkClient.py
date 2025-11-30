import socket
import subprocess
import time

class NetworkClient:
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.ip == "":
            self.ip = self.get_local_wifi_ip()

        try:
            self.client_socket.connect((self.ip, self.port))
        except Exception:
            subprocess.Popen(["python", "collabServer.py"])
            time.sleep(2)
            self.client_socket.connect((self.ip, self.port))
    
    def get_local_wifi_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except:
            return "127.0.0.1"
        finally:
            s.close()

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
