import socket
import os

# Function to handle user login
def login(s):
    username = input("Enter username: ")
    s.send(username.encode("utf-8"))
    password = input("Enter password: ")
    s.send(password.encode("utf-8"))
    response = s.recv(1024).decode("utf-8")
    if response == "Login successful":
        print("Login successful")
    else:
        print("Login failed")
    return response == "Login successful"


# Function to send an HTTP request to the server
def send_http_request(s, host="127.0.0.1"):
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
    s.sendall(request.encode("utf-8"))
    response = s.recv(4096).decode("utf-8")
    print(f"HTTP response:\n{response}")


if __name__ == "__main__":
    try:
        # Create a socket and connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9095))

        if not login(s):
            s.close()
            exit()

        while True:
            # Send commands to the server
            command = input("Enter command or message to send to server: ")
            s.send(command.encode("utf-8"))

            if command == "bye":
                break

            if command == "http":
                # Send an HTTP request to the server
                send_http_request(s)
                continue

            elif command == "dir":
                # Receive and print list of files from the server
                files = s.recv(1024).decode("utf-8")
                print(files)

            elif command.startswith("download "):
                # Handle file download from the server
                filename = command.split()[1]
                response = s.recv(4096).decode("utf-8")

                if response == "FILE_NOT_FOUND":
                    print(f"Error: File {filename} does not exist on server")
                    continue

                if response.startswith("FILE_SIZE:"):
                    file_size = int(response.split(":")[1])
                    new_filename = (
                        filename.split(".")[0] + "_download." + filename.split(".")[1]
                    )

                    with open(new_filename, "wb") as f:
                        received_size = 0
                        while received_size < file_size:
                            file_data = s.recv(4096)
                            f.write(file_data)
                            received_size += len(file_data)

                    print(
                        f"File {filename} downloaded successfully, saved as {new_filename}"
                    )

            elif command.startswith("upload "):
                # Handle file upload to the server
                filename = command.split()[1]
                if os.path.exists(filename):
                    response = s.recv(1024).decode("utf-8")
                    if response.startswith("REJECTED:"):
                        print(f"Upload rejected: {response.split(':')[1]}")
                        continue

                    if response == "READY":
                        file_size = os.path.getsize(filename)
                        s.send(f"FILE_SIZE:{file_size}".encode("utf-8"))

                        with open(filename, "rb") as f:
                            while True:
                                file_data = f.read(4096)
                                if not file_data:
                                    break
                                s.sendall(file_data)

                        response = s.recv(1024).decode("utf-8")
                        print(response)
                else:
                    print("File does not exist")

    except Exception as e:
        print("Error: ", e)
    finally:
        s.close()
