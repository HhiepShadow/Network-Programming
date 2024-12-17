import socket

def start():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9095))
    try:
        while True:   
            message = input("Enter message to server: ")
            if message.lower() == "bye":
                break
            client_socket.send(message.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')
            if response.lower() == "bye":
                print(f"Message from server: {response}")
                break
    finally:
        client_socket.close()

if __name__ == "__main__":
    start()