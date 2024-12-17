import socket

if __name__ == '__main__':
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sk.bind(('127.0.0.1', 9050))

    data, address = sk.recvfrom(1024)

    print(f"Client send: {data}")

    data = 'Hello Client'

    sk.sendto(data.encode('utf-8'), address)

    sk.close()
