import socket 

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

    s.connect(('127.0.0.1', 9050))

    data = s.recv(4096)

    print(f"Receive from server: {data.decode('utf-8')}")

    data = "Hello Server"
    s.send(data.encode('utf-8'))

    s.close()