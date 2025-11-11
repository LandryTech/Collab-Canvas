from networkServer import NetworkServer

def main():
    server = NetworkServer('127.0.0.1', 5000)
    server.start()

if __name__ == "__main__":
    main()