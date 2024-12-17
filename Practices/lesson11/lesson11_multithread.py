import socket
import threading

host = '127.0.0.1'
port = 9050

def create_socket(host: str, port: int) -> socket.socket:
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sk.bind((host, port))
    sk.listen(10)

    return sk

def receive_msg(sk: socket.socket) -> None:
    data = bytearray()
    msg = ''

    while not msg:
        b = sk.recv(1024)
        if not b:
            raise ConnectionError()
        
        data = data + b

        if b'\0' in b:
            msg = data.rstrip(b'\0')
    msg = msg.decode('utf-8')
    return msg

def create_msg(msg):
    msg = msg + '\0'
    return msg.encode('utf-8')

def send_msg(sk: socket.socket, msg):
    data = create_msg(msg)
    sk.sendall(data)

def process_client(sk, addr):
    try:
        msg = receive_msg(sk)
        msg = f"{addr}: {msg}"
        print(msg)
        send_msg(sk, msg)
    except ConnectionError as e:
        print(f"Error: {e}")
    finally:
        print("Socket closed")
        sk.close()

if __name__ == '__main__':
    sk = create_socket(host, port)

    addr = sk.getsockname()
    print(f"Dia chi cuc bo: {addr}")

    # while True:
    #     client_socket, client_addr = sk.accept()
    #     print(f"Dia chi client: {client_addr}")

    #     try:
    #         msg = receive_msg(client_socket)
    #         print(f"{client_socket}: {msg}")
    #         send_msg(client_socket, msg)
    #     except ConnectionError as e:
    #         print(f"Error: {e}")
    #     finally:
    #         print(f"Stop connection: {client_addr}")
    #         client_socket.close()
    while True:
        client_socket, client_addr = sk.accept()
        print(f"Dia chi client: {client_addr}")
        thread = threading.Thread(target=process_client, args=[client_socket, addr], daemon=True)
        thread.start()
        print(f"Connect from {addr}")

