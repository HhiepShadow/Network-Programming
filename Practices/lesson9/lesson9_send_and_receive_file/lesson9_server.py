# import socket
# import os

# def list_files():
#     return os.listdir('.')

# def start_server(host='127.0.0.1', port=9050):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((host, port))
#         s.listen()
#         print(f"Server đang chạy tại {host}:{port}...")
#         conn, addr = s.accept()
#         with conn:
#             print(f"Kết nối từ {addr}")
            
#             while True:
#                 command = conn.recv(1024).decode('utf-8')
#                 if command.lower() == 'dir':
#                     # Gửi danh sách file
#                     files = list_files()
#                     conn.sendall('\n'.join(files).encode('utf-8'))
#                 elif command.lower().startswith('get '):
#                     filename = command[4:]  # Lấy tên file từ lệnh 'get filename'
#                     print(f"Nhận yêu cầu gửi file: {filename}")
                    
#                     # Gửi file
#                     if os.path.exists(filename):
#                         with open(filename, 'rb') as f:
#                             data = f.read(1024)
#                             while data:
#                                 conn.sendall(data)
#                                 data = f.read(1024)
#                         print(f"Đã gửi file: {filename}")
#                     else:
#                         print(f"File không tồn tại: {filename}")
#                 else:
#                     print("Lệnh không hợp lệ")
# if __name__ == "__main__":
#     start_server()

import socket
import os
from datetime import datetime

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

            elif command == "dir":
                # List files in the current directory
                files = os.listdir(".")
                files_list = "\n".join(files)
                client_socket.send(files_list.encode("utf-8"))

            elif command.startswith("get "):
                # Send file to client
                filename = command.split()[1]
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    client_socket.send(f"FILE_SIZE:{file_size}".encode("utf-8"))
                    with open(filename, "rb") as f:
                        while True:
                            file_data = f.read(4096)
                            if not file_data:
                                break
                            client_socket.send(file_data)
                else:
                    client_socket.send("File does not exist".encode("utf-8"))

            else:
                # Send custom message to client
                message = input("Enter data to send to client: ")
                client_socket.send(message.encode("utf-8"))
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
