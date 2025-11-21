# 10.30.72.77 - Emerson eduroam

from networkClient import NetworkClient

def main():
    client = NetworkClient("10.30.72.77", 5002)
    print("Connected! Type messages to send. Type 'exit' to quit.\n")

    while True:
        msg = input("> ")
        if msg.lower() == "exit":
            client.stop()
            break

        client.send(msg)
        response = client.receive()
        if response:
            for part in response:
                print("Received: ", part)

if __name__ == "__main__":
    main()