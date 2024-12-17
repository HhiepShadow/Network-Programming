import socket
import threading
import os
from datetime import datetime

# Lấy đường dẫn tuyệt đối cho các file trong thư mục Server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
accounts_file = os.path.join(BASE_DIR, "accounts.txt")
logs_file = os.path.join(BASE_DIR, "logs.txt")
uploads_dir = os.path.join(BASE_DIR, "uploads")

# Tạo thư mục uploads nếu chưa tồn tại
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

def handle_client(client_socket, client_address):
    print(f"NEW CONNECTION {client_address} connected.")
    client_socket.send("Please login: ".encode("utf-8"))
    account_data = client_socket.recv(1024).decode("utf-8")
    
    username, password = account_data.split(',')
    if validate_user(username, password):
        client_socket.send("Login successful!\n".encode("utf-8"))
        log_action(username, "Login")
    else:
        client_socket.send("Not found account.\n".encode("utf-8"))
        client_socket.close()
        return

    while True:
        try:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break
            
            command, *args = request.split()
            
            if command == "upload":
                if args:
                    filename = args[0]
                    client_socket.send("OK".encode("utf-8"))  # Thông báo để client bắt đầu gửi file
                    receive_file(client_socket, filename)
                    log_action(username, f"Upload: {filename}")
                    client_socket.send(f"File {filename} uploaded successful.\n".encode("utf-8"))
                else:
                    client_socket.send("Missing file name to upload.\n".encode("utf-8"))
            
            elif command == "download":
                if args:
                    filename = args[0]
                    send_file(client_socket, filename)
                    log_action(username, f"Download: {filename}")
                else:
                    client_socket.send("Missing file name to download.\n".encode("utf-8"))
            
            elif command == "logout":
                log_action(username, "Logout")
                break

        except Exception as e:
            print(f"Lỗi với client {client_address}: {e}")
            break

    client_socket.close()
    print(f"[DISCONNECT] {client_address} disconnected.")

def validate_user(username, password):
    try:
        with open(accounts_file, "r") as f:
            for line in f:
                user, passw = line.strip().split(',')
                if username == user and password == passw:
                    return True
    except FileNotFoundError:
        print("File accounts.txt not exist.")
    return False

def log_action(username, action):
    with open(logs_file, "a") as log_file:
        log_file.write(f"{datetime.now()} - {username}: {action}\n")

def receive_file(client_socket, filename):
    upload_path = os.path.join(uploads_dir, filename)  # Ghi file vào thư mục uploads
    with open(upload_path, "wb") as f:
        while True:
            data = client_socket.recv(1024)
            if data == b"EOF":  # Nhận tín hiệu kết thúc
                break
            f.write(data)
    print(f"RECEIVE File {filename} is uploaded successful.")

def send_file(client_socket, filename):
    if os.path.exists(os.path.join(uploads_dir, filename)):
        with open(os.path.join(uploads_dir, filename), "rb") as f:
            data = f.read(1024)
            while data:
                client_socket.send(data)
                data = f.read(1024)
        client_socket.send(b"EOF")  # Gửi tín hiệu kết thúc
        print(f"SEND File {filename} is sent successful.")
    else:
        client_socket.send("File is not found.\n".encode("utf-8"))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("34.124.137.135", 21))
    server_socket.listen(5)
    print("LISTENING Server is listening...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

start_server()
