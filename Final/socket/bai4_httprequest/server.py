import socket
import os
from datetime import datetime
import threading

users_db = {
    "user1": "123",
    "user2": "456",
}

# Function to log server activities
def log_activity(activity):
    with open("server_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {activity}\n")


# Function to check if a file is unsafe
def is_unsafe_file(filename):
    # List of unsafe file extensions
    unsafe_extensions = {".exe", ".bat", ".cmd", ".sh", ".ps1", ".vbs"}
    return os.path.splitext(filename)[1].lower() in unsafe_extensions


# Function to handle HTTP requests
def handle_http_request(request):
    headers = request.split("\r\n")
    print(headers)
    if headers[0].startswith("GET"):
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response += "<html><body><h1>Hello</h1></body></html>"
    else:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"
    return response


# Function to handle client connections
def handle_client(client_socket):
    try:
        # Receive username and password from client
        username = client_socket.recv(1024).decode("utf-8")
        password = client_socket.recv(1024).decode("utf-8")

        # Check if the credentials are valid
        if username in users_db and users_db[username] == password:
            client_socket.send("Login successful".encode("utf-8"))
            log_activity(f"User {username} logged in")
            print(f"User {username} logged in")
        else:
            client_socket.send("Login failed".encode("utf-8"))
            client_socket.close()
            return

        while True:
            # Receive command from client
            command = client_socket.recv(1024).decode("utf-8")
            if not command:
                break

            print(f"Message from {username}: {command}")

            if command == "bye":
                log_activity(f"User {username} logged out")
                print(f"User {username} logged out")
                break

            elif command == "http":
                # Receive the actual HTTP request
                http_request = client_socket.recv(4096).decode("utf-8")
                response = handle_http_request(http_request)
                client_socket.sendall(response.encode("utf-8"))
                log_activity(f"User {username} sent an HTTP request")

            elif command == "dir":
                # Send list of files in the current directory
                files = os.listdir(".")
                files_list = "\n".join(files)
                client_socket.send(files_list.encode("utf-8"))

            elif command.startswith("download "):
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
                    log_activity(f"{username} downloaded {filename}")
                else:
                    client_socket.send("FILE_NOT_FOUND".encode("utf-8"))
                    log_activity(
                        f"{username} attempted to download non-existent file {filename}"
                    )

            elif command.startswith("upload "):
                filename = command.split()[1]
                if is_unsafe_file(filename):
                    client_socket.send("REJECTED:Unsafe file type".encode("utf-8"))
                    log_activity(
                        f"{username} attempted to upload unsafe file {filename}"
                    )
                    continue

                client_socket.send("READY".encode("utf-8"))
                response = client_socket.recv(1024).decode("utf-8")

                if response.startswith("FILE_SIZE:"):
                    file_size = int(response.split(":")[1])
                    with open(filename, "wb") as f:
                        received_size = 0
                        while received_size < file_size:
                            file_data = client_socket.recv(4096)
                            if not file_data:
                                break
                            f.write(file_data)
                            received_size += len(file_data)

                    if received_size == file_size:
                        client_socket.send("Upload successful".encode("utf-8"))
                        log_activity(f"{username} uploaded {filename}")
                    else:
                        client_socket.send(
                            "Upload failed: Incomplete file".encode("utf-8")
                        )
                        log_activity(f"{username} failed to upload {filename}")
                else:
                    client_socket.send("Failed to receive file size".encode("utf-8"))

            else:
                client_socket.send("Invalid command".encode("utf-8"))

    except socket.error as e:
        print("Error: ", e)
    finally:
        client_socket.close()


if __name__ == "__main__":
    try:
        # Create a socket and bind it to the local address
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 9095))
        s.listen(5)
        print("Server is listening on port 9095")

        while True:
            # Accept client connections
            client_socket, client_address = s.accept()
            print("Client address: ", client_address)
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket,)
            )
            client_handler.start()
    except socket.error as e:
        print("Error: ", e)
    finally:
        s.close()
