import socket

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9095))

    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            print(f"Message from server: {data.decode('utf-8')}")

            if data.decode('utf-8') == "bye":
                break
            command = input("Enter command: ")
            s.send(command.encode('utf-8'))
            