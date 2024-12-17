import socket
import threading

def handle_client(client_socket: socket.socket, client_address):
    print(f"Connected with: {client_address}")

    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                break 
            print(f"Message from {client_address}")

            response = input("Enter message to respond to client: ")
            client_socket.send(response.encode("utf-8"))
    except ConnectionError as err:
        print(f"Error: {err}")
    finally:
        client_socket.close()
        print(f"Disconnected with: {client_address}")


def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', 9095))
    server_socket.listen(5)
    print("Server is listening on port 9095")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) 
        client_thread.start()

if __name__ == '__main__':
    start()
