import socket
import os
from datetime import datetime
import string

def handle_client(client_socket):
    try:
        # Send current time to client when they first connect
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_socket.send(f"Connected at: {current_time}".encode("utf-8"))

        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            command = data.decode("utf-8")
            print("Message from client: ", command)

            if command == "bye":
                client_socket.send("bye".encode("utf-8"))
                break
            
            # client_socket.send(message.encode("utf-8"))
    except socket.error as e:
        print("Error: ", e)
    finally:
        client_socket.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 9095))
    s.listen(5)
    print("Server is listening on port 9095")

    try:
        while True:
            client_socket, client_address = s.accept()
            print("Client address: ", client_address)
            handle_client(client_socket)
    except socket.error as e:
        print("Error: ", e)
    finally:
        s.close()
