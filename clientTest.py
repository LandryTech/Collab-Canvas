from networkClient import NetworkClient

def main():
    client = NetworkClient("127.0.0.1", 5000)

    print("Connected to server! Type a message and press Enter.")
    while True:
        msg = input("> ")
        if msg.lower() == "exit":
            print("Closing connection.")
            break
        client.send(msg)
        try:
            response = client.receive()
            print("Received:", response)
        except:
            print("Server disconnected.")
            break

if __name__ == "__main__":
    main()
