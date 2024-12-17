import socket
import os
from datetime import datetime
import string

students_db = {
    "12345": {"Hoten": "Nguyen Van A", "DTB": 7.8},
    "67890": {"Hoten": "Tran Thi B", "DTB": 8.2},
    "11223": {"Hoten": "Le Van C", "DTB": 6.5},
}
 
 
def convert_string(s):
    # Loai bo khoang trong o dau va cuoi chuoi
    s = s.strip()
    # Loai bo khoang trong o giua cac tu
    s = " ".join(s.split())
    # Xu ly dau phay
    s = ", ".join([part.strip() for part in s.split(",")])
 
    # Xu ly dau cham
    sentences = s.split(".")
    sentences = [sentence.strip().capitalize() for sentence in sentences if sentence]
    s = ". ".join(sentences)
 
    # them dau cau vao ky tu cuoi cung cua chuoi
    if s and s[-1] not in string.punctuation:
        s += "."
 
    return s
 
 
def handle_client(client_socket):
    try:
        # Gửi thời gian hiện tại khi client mới kết nối
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_socket.send(f"Connected at: {current_time}".encode("utf-8"))
 
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            command = data.decode("utf-8")
            print("Message from client: ", command)
 
            if command == "bye":
                client_socket.send("bye".encode("utf-8"))
                break
 
            elif command == "dir":
                # Liệt kê danh sách file trong thư mục hiện tại
                files = os.listdir(".")
                files_list = "\n".join(files)
                client_socket.send(files_list.encode("utf-8"))
 
            elif command.startswith("get "):
                # Gửi file cho client
                filename = command.split()[1]
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    client_socket.send(f"FILE_SIZE:{file_size}".encode("utf-8"))
                    with open(filename, "rb") as f:
                        while True:
                            file_data = f.read(4096)
                            if not file_data:
                                break
                            client_socket.send(file_data)
                else:
                    client_socket.send("File does not exist".encode("utf-8"))
 
            elif command.startswith("convert "):
                # Chuan hoa chuoi va gui cho client
                string_to_convert = command[len("convert ") :]
                new_string = convert_string(string_to_convert)
                client_socket.send(new_string.encode("utf-8"))
 
            elif command.startswith("find "):
                # Tim kiem sinh vien trong database
                masv = command.split()[1]
                if masv in students_db:
                    student_info = students_db[masv]
                    response = f"MASV: {masv}, Hoten: {student_info['Hoten']}, DTB: {student_info['DTB']}"
                else:
                    response = "None"
                client_socket.send(response.encode("utf-8"))
 
            else:
                # Gửi thông điệp khác cho client
                message = input("Enter data to send to client: ")
                client_socket.send(message.encode("utf-8"))
    except socket.error as e:
        print("Error: ", e)
    finally:
        client_socket.close()
 
 
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 9095))
    s.listen(5)
    print("Server is listening on port 9095")
 
    try:
        while True:
            client_socket, client_address = s.accept()
            print("Client address: ", client_address)
            handle_client(client_socket)
    except socket.error as e:
        print("Error: ", e)
    finally:
        s.close()