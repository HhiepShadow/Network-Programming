import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9095))
 
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            print("Message from server: ", data.decode("utf-8"))
 
            if data.decode("utf-8") == "bye":
                break
            command = input("Enter command or message to send to server: ")
            s.send(command.encode("utf-8"))
 
            if command.startswith("get "):
                # Nhận file từ server
                filename = command.split()[1]
                new_filename = (
                    filename.split(".")[0] + "_download." + filename.split(".")[1]
                )
                response = s.recv(4096).decode("utf-8")
                if response.startswith("FILE_SIZE:"):
                    file_size = int(response.split(":")[1])
 
                    with open(new_filename, "wb") as f:
                        received_size = 0
                        while received_size < file_size:
                            file_data = s.recv(4096)
                            f.write(file_data)
                            received_size += len(file_data)
 
                    print(
                        f"File {filename} downloaded successfully, saved as{new_filename}"
                    )
                    s.send("Client received file successfully".encode("utf-8"))
 
                    # Đọc và in nội dung file vừa tải
                    with open(new_filename, "r") as f:
                        print(f"Content of {new_filename}:")
                        print(f.read())
                elif response == "File does not exist":
                    print(response)
 
            if command.startswith("convert "):
                # Nhan chuoi vua dc xu ly tu server
                converted_string = s.recv(4096).decode("utf-8")
                s.send("Client received converted string successfully".encode("utf-8"))
                print("Converted string from server: ", converted_string)
 
            if command.startswith("find "):
                # Nhan thong tin sinh vien tu server
                student_info = s.recv(4096).decode("utf-8")
                s.send("Client received info successfully".encode("utf-8"))
                print("Response from server: ", student_info)
 
    except socket.error as e:
        print("Error: ", e)
    finally:
        s.close()