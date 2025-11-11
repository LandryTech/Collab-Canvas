from networkServer import NetworkServer

def main():
    server = NetworkServer('', 5002)
    server.start()

if __name__ == "__main__":
    main()