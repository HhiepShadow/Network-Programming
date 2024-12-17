import socket

if __name__ == "__main__":
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
    s.bind(('127.0.0.1', 9050))
    
    while 1:
        try:
            s.listen(5)

            client_socket, client_addr = s.accept()
            print(f"Client address: {client_addr}")
        except socket.error as e:
            print("Connection failed: {e}")

        while 1:
            data = input("Enter text: ")

            client_socket.send(data.encode("utf-8"))

            data = client_socket.recv(4096)

            print(f"Receive from client: {data.decode("utf-8")}")

            if data.decode('utf-8') == "bye":
                client_socket.send("bye".encode('utf-8'))
                client_socket.close()
                break
        s.close()
        