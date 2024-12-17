import socket

def handle_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9095))

    try:
        while True:
            request = input("Enter your command: ")
            if request.lower() == "upload":
                filename = input("Enter your filename to upload: ")
                client_socket.send(f"upload {filename}".encode("utf-8"))
                
                with open(filename, "rb") as f:
                    data = f.read(4096)
                    while data:
                        client_socket.send(data)
                        data = f.read(4096)
                    client_socket.send(b"EOF")
            elif request.lower().startswith("download"):
                filename = input("Enter your filename to download: ")
                client_socket.send(f"download {filename}".encode("utf-8"))

                with open(f"downloaded_{filename}", "wb") as f:
                    while True:
                        data = client_socket.recv(4096)
                        if not data or data == b"EOF":
                            break 
                        f.write(data)
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

handle_server()