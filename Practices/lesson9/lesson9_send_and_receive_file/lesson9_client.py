# import socket

# def request_file(host='127.0.0.1', port=9050):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((host, port))
        
#         while True:
#             command = input("Nhập lệnh (dir để hiển thị file, exit để thoát): ")
#             if command.lower() == 'dir':
#                 # Gửi lệnh dir đến server
#                 s.sendall(command.encode('utf-8'))
                
#                 # Nhận danh sách file
#                 files = s.recv(1024).decode('utf-8')
#                 print("Danh sách file trên server:")
#                 print(files)
                
#                 # Gửi tên file muốn nhận
#                 filename_to_request = input("Nhập tên file muốn nhận (hoặc gõ exit để thoát): ")
#                 if filename_to_request.lower() == 'exit':
#                     break
#                 s.sendall(f'get {filename_to_request}'.encode('utf-8'))
                
#                 # Nhận file
#                 with open('received_' + filename_to_request, 'wb') as f:
#                     while True:
#                         data = s.recv(1024)
#                         if not data:
#                             break
#                         f.write(data)
#                 print(f"Đã nhận file: {filename_to_request}")
#             elif command.lower() == 'exit':
#                 break
#             else:
#                 print("Lệnh không hợp lệ. Vui lòng thử lại.")

# if __name__ == "__main__":
#     request_file()

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
                # Get file from server
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

                    # Read and print the content of the file
                    with open(new_filename, "r") as f:
                        print(f"Content of {new_filename}:")
                        print(f.read())
                elif response == "File does not exist":
                    print(response)

    except socket.error as e:
        print("Error: ", e)
    finally:
        s.close()
