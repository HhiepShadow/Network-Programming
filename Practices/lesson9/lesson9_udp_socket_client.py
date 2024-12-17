import socket

if __name__ == '__main__':
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    data = 'Hello Server'
    sk.sendto(data.encode('utf-8'), ('127.0.0.1', 9050))
    
    data = sk.recvfrom(1024)

    print(f"Server send: {data}")

    sk.close()