from networkServer import NetworkServer

def main():
    server = NetworkServer('0.0.0.0', 5002)
    server.start()

if __name__ == "__main__":
    main()