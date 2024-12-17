import socket

def request_file(host='127.0.0.1', port=9050):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while True:
            command = input("Nhập lệnh (dir để hiển thị file, exit để thoát): ")
            if command.lower() == 'dir':
                # Gửi lệnh dir đến server
                s.sendall(command.encode('utf-8'))
                
                # Nhận danh sách file
                files = s.recv(1024).decode('utf-8')
                print("Danh sách file trên server:")
                print(files)
                
                # Gửi tên file muốn nhận
                filename_to_request = input("Nhập tên file muốn nhận (hoặc gõ exit để thoát): ")
                if filename_to_request.lower() == 'exit':
                    break
                s.sendall(f'get {filename_to_request}'.encode('utf-8'))
                
                # Nhận file
                with open('received_' + filename_to_request, 'wb') as f:
                    while True:
                        data = s.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(f"Đã nhận file: {filename_to_request}")
            elif command.lower() == 'exit':
                break
            else:
                print("Lệnh không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    request_file()