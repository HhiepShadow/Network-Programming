import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', 9095))
        while True:
            message = input("Enter message to server: ")
            client_socket.send(message.encode("utf-8"))

            if message.startswith("find "):
                data = client_socket.recv(4096).decode("utf-8")
                print(f"Response from server: {data}")
    except socket.error as err:
        print(f"Error: {err}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
