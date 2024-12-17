import socket 
import threading

STUDENT_DB = {
    "12345": {
        "Fullname": "Nguyen Van A",
        "DTB": 8.0
    },
    "23456": {
        "Fullname": "Nguyen Van B",
        "DTB": 9.0
    },
    "34567": {
        "Fullname": "Nguyen Van C",
        "DTB": 10.0
    }
}

def handle_client(client_socket: socket.socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            command = data.decode('utf-8')
            print(f"Message from client: {command}")

            if command == "bye":
                client_socket.send("bye".encode("utf-8"))
                break 
            elif command.startswith("find "):
                masv = command.split(' ')[1]
                if masv in STUDENT_DB:
                    student_info = STUDENT_DB[masv]
                    response = f"MaSV: {masv} - HoTen: {student_info['Fullname']} - DTB: {student_info['DTB']}"
                else:
                    response = "None"
                client_socket.send(response.encode('utf-8'))
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 9095))
    s.listen(5)

    try:
        while True:
            client_socket, client_addr = s.accept()
            print(f"Client address: {client_addr}")
            handle_client(client_socket)
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        s.close()