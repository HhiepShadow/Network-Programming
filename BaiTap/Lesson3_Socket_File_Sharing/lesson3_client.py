import socket

def main():
    server_ip = input("Enter the server IP address: ")
    server_port = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    client_socket.send(username.encode())
    client_socket.send(password.encode())
    
    response = client_socket.recv(1024).decode()
    print(response)

    if response == 'Login successful':
        while True:
            command = input("Enter command (UPLOAD, DOWNLOAD, EXIT): ")

            if command == 'UPLOAD':
                filename = input("Enter filename to upload: ")
                client_socket.send(command.encode())
                client_socket.send(filename.encode())
                with open(filename, 'rb') as f:
                    data = f.read(1024)
                    while data:
                        client_socket.send(data)
                        data = f.read(1024)
                print(client_socket.recv(1024).decode())

            elif command == 'DOWNLOAD':
                filename = input("Enter filename to download: ")
                client_socket.send(command.encode())
                client_socket.send(filename.encode())
                response = client_socket.recv(1024).decode()
                if response == 'EXISTS':
                    with open('downloaded_' + filename, 'wb') as f:
                        data = client_socket.recv(1024)
                        while data:
                            f.write(data)
                            data = client_socket.recv(1024)
                    print("File downloaded successfully.")
                else:
                    print("File not found on server.")

            elif command == 'EXIT':
                client_socket.send(command.encode())
                client_socket.close()
                break
    else:
        print("Login failed. Exiting.")

if __name__ == "__main__":
    main()