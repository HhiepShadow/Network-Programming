import socket
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
upload_dir = os.path.join(BASE_DIR, "uploads")

def receive_file(client_socket: socket.socket, filename):
    upload_file = os.path.join(upload_dir, filename)
    try:
        with open(upload_file, "wb") as f:
            while True:
                data = client_socket.recv(4096)
                if data == b"EOF":
                    break 
                f.write(data)
    except FileNotFoundError as e:
        print(f"Error: {e}")

def send_file(client_socket: socket.socket, filename):
    if os.path.exists(os.path.join(upload_dir, filename)):
        with open(os.path.join(upload_dir, filename), "rb") as f:
            data = f.read(4096)
            while data:
                client_socket.send(data)
                data = f.read(4096)
            client_socket.send(b"EOF")
    else:
        client_socket.send("Download failed")


def handle_client(client_socket: socket.socket, client_address):
    print(f"NEW CONNECTION: {client_address}")

    try:
        while True:
            request = client_socket.recv(4096).decode("utf-8")
            if request.lower().startswith("upload"):
                command, *args = request.split()
                if args:
                    filename = args[0]
                    receive_file(client_socket, filename)
            elif request.lower().startswith("download"):
                command, *args = request.split()
                if args:
                    filename = args[0]
                    send_file(client_socket, filename)
    except socket.error as e:
        print(f"Error: {e}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9095))
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

start_server()