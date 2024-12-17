import socket
import threading

def receive_message(client_socket: socket.socket):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(message)
    except ConnectionResetError:
        print("Disconnected from server")
    finally:
        client_socket.close()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(("127.0.0.1", 9095))

    thread = threading.Thread(target=receive_message, args=(client_socket,))
    thread.start()

    try: 
        while True:
            message = input()
            if message.lower() == "exit":
                print("Disconnecting...")
                break
            client_socket.send(message.encode("utf-8"))
    except KeyboardInterrupt:
        print("Exiting chat...")
    finally:
        client_socket.close()

start_client()