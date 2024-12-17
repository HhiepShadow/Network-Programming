import socket
import threading

clients = []

def handle_client(client_socket: socket.socket, client_address):
    print(f"New connection: {client_address}")

    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break 
            broadcast(message, client_socket)
    except ConnectionResetError:
        print(f"Client {client_address} disconnected unexpectedly")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection closed: {client_address}")

def broadcast(message, client_socket: socket.socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except socket.error as e:
                pass

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 9095))
    server_socket.listen(5)
    print("Server is listening...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

start_server()
    
