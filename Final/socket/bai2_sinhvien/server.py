import socket 
import threading

student_db = {
    "12345": {
        "HoTen": "Nguyen Van A",
        "DTB": 9.0
    },
    "23456": {
        "HoTen": "Tran Thi B",
        "DTB": 8.5
    },
    "34567": {
        "HoTen": "Le Van C",
        "DTB": 8.0
    }
}

def handle_client(client_socket: socket.socket, client_address):
    print(f"Connected with: {client_address}")
    try:
        while True:
            data = client_socket.recv(4096).decode("utf-8")
            if not data:
                break 
            print(f"Message from {client_address}: {data}")

            if data == "bye":
                print(f"Disconnected from {client_address}")
                client_socket.send("bye".encode("utf-8"))
                break 

            elif data.startswith("find "):
                masv = data.split(' ')[1]
                if masv in student_db:
                    student_info = student_db[masv]
                    response = f"MASV: {masv} - HoTen: {student_info['HoTen']}, DTB: {student_info['DTB']}"
                else:
                    response = "None"
                client_socket.send(response.encode("utf-8"))
            else:
                message = input("Enter message to respond client: ")
                client_socket.send(message.encode("utf-8"))
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9095))
    server_socket.listen(5)
    print(f"Server is listening on port 9095")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
