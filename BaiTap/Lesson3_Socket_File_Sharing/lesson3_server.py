import socket
import os
import threading

USER_CREDENTIALS = {
    'user1': 'pass1',
    'user2': 'pass2'
}

LOG_FILE = './Lesson3_Socket_File_Sharing/file_transfer_log.txt'

def log_activity(action, filename, client_address):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{action} | {filename} | {client_address}\n")

def handle_client(client_socket):
    # Nhận thông tin đăng nhập
    username = client_socket.recv(1024).decode()
    password = client_socket.recv(1024).decode()

    if USER_CREDENTIALS.get(username) == password:
        client_socket.send(b'Login successful')
        print(f"{username} logged in.")
    else:
        client_socket.send(b'Login failed')
        client_socket.close()
        return

    while True:
        command = client_socket.recv(1024).decode()
        
        if command == 'UPLOAD':
            filename = client_socket.recv(1024).decode()
            with open(filename, 'wb') as f:
                data = client_socket.recv(1024)
                while data:
                    f.write(data)
                    data = client_socket.recv(1024)
            log_activity('UPLOAD', filename, client_socket.getpeername())
            client_socket.send(b'File uploaded successfully')

        elif command == 'DOWNLOAD':
            filename = client_socket.recv(1024).decode()
            if os.path.exists(filename):
                client_socket.send(b'EXISTS')
                with open(filename, 'rb') as f:
                    data = f.read(1024)
                    client_socket.send(data)
                    while data:
                        data = f.read(1024)
                        client_socket.send(data)
                log_activity('DOWNLOAD', filename, client_socket.getpeername())
            else:
                client_socket.send(b'NOT FOUND')

        elif command == 'EXIT':
            client_socket.close()
            break

def start_server(host='0.0.0.0', port=5001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on port", port)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()