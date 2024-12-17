import socket
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(BASE_DIR, "uploads")

def handle_client(client_socket: socket.socket, client_addr: str) -> None:
    print(f"New connection: {client_addr}")
    client_socket.send("Please login: ".encode('utf-8'))
    
    username = client_socket.recv(4096).decode('utf-8')
    print(f"Username: {username}")
    password = client_socket.recv(4096).decode('utf-8')
    print(f"Password: {password}")

    if validate_user(username, password):
        client_socket.send("Login successful".encode('utf-8'))
    else:
        client_socket.send("Not found account".encode('utf-8'))
        client_socket.close()
        return 
    
    while True:
        try:
            request = client_socket.recv(4096).decode('utf-8')
            if not request:
                break 

            command, *args = request.split()

            if command == "upload":
                if args:
                    filename = args[0]
                    client_socket.send(f"Received filename: {filename}".encode('utf-8'))
                    receive_file(client_socket, filename)
                else:
                    client_socket.send("Missing file name\n")
            elif command == "download":
                if args:
                    filename = args[0]
                    send_file(client_socket, filename)
                else:
                    client_socket.send("Missing file name")
            elif command == "logout":
                break 
            
        except socket.error as e:
            print(f"Error: {e}")
    client_socket.close()
    print(f"Disconnect {client_addr}")

def validate_user(username, password) -> bool:
    return username == 'test' and password == 'LapTrinhMang@2024'

def receive_file(client_socket: socket.socket, filename: str):
    upload_path = os.path.join(uploads_dir, filename)

    try: 
        with open(upload_path, 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if data == b"EOF":
                    break 
                f.write(data)
        print(f"Received file successfully")
    except FileNotFoundError as e:
        print(f"Error: {e}")

def send_file(client_socket: socket.socket, filename: str):
    if os.path.exists(os.path.join(uploads_dir, filename)):
        with open(os.path.join(uploads_dir, filename), 'rb') as f:
            data = f.read(4096)
            while data:
                client_socket.send(data)
                data = f.read(4096)
        client_socket.send(b"EOF")
        print(f"Send file successfully")
    else:
        client_socket.send("File is not found")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    print("LISTENING Server is listening...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

start_server()