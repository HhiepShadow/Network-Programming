import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))
    
    print(client_socket.recv(1024).decode("utf-8"))  # Nhận thông báo đăng nhập
    username = input("Enter username: ")
    client_socket.send(username.encode('utf-8'))
    password = input("Enter password: ")
    client_socket.send(password.encode('utf-8'))
    client_socket.send(f"{username},{password}".encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    print(response)

    if "Login successful" in response:
        while True:
            command = input("Enter command (upload/download/logout): ")
            if command.startswith("upload"):
                filename = input("Enter file name to upload: ")
                client_socket.send(f"upload {filename}".encode("utf-8"))  # Gửi lệnh upload
                response = client_socket.recv(1024).decode("utf-8")  # Nhận OK từ server
                if response == "OK":
                    with open(filename, "rb") as f:
                        data = f.read(1024)
                        while data:
                            client_socket.send(data)
                            data = f.read(1024)
                    client_socket.send(b"EOF")  # Gửi tín hiệu EOF để báo kết thúc
                    print(f"Đã upload {filename}.")
                else:
                    print("Server is not ready to upload.")
            elif command.startswith("download"):
                filename = input("Enter file name to download: ")
                client_socket.send(f"download {filename}".encode("utf-8"))
                with open("downloaded_" + filename, "wb") as f:
                    while True:
                        data = client_socket.recv(1024)
                        if data == b"EOF":
                            break
                        f.write(data)
                print(f"Downloaded {filename}.")
            elif command == "logout":
                client_socket.send(b"logout")
                break
    
    client_socket.close()

client_program()
