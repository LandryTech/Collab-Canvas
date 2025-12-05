""" PURPOSE
—COLLAB SERVER—
A program that starts the server for Collab Canvas.
This must run before WhiteboardUI is started.
"""

from networkServer import NetworkServer

IP = '0.0.0.0'
PORT = 5002

def main():
    server = NetworkServer(IP, PORT)
    server.start()

if __name__ == "__main__":
    main()