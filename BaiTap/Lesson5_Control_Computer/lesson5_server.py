import cv2
import socket
import struct
import pickle
import numpy as np
import threading

# Cấu hình server
HOST = '0.0.0.0'  # Lắng nghe từ mọi IP
PORT_SCREEN = 9999  # Port cho việc nhận hình ảnh
PORT_CONTROL = 10000  # Port cho điều khiển từ xa

# Tạo socket để nhận màn hình
screen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen_socket.bind((HOST, PORT_SCREEN))
screen_socket.listen(1)

# Tạo socket cho điều khiển từ xa
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_socket.bind((HOST, PORT_CONTROL))
control_socket.listen(1)

print("Đang chờ kết nối từ client...")
client_screen, screen_address = screen_socket.accept()
client_control, control_address = control_socket.accept()
print(f"Kết nối từ {screen_address} và {control_address}")

# Khởi tạo biến toàn cục cho khung hình để cập nhật trong luồng GUI
frame = None
frame_lock = threading.Lock()

def display_screen():
    global frame
    while True:
        with frame_lock:
            if frame is not None:
                cv2.imshow("Remote Screen", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

# Tạo và khởi động thread cho GUI
gui_thread = threading.Thread(target=display_screen)
gui_thread.start()

try:
    while True:
        # Nhận dữ liệu màn hình
        data = b""
        payload_size = struct.calcsize("L")
        
        while len(data) < payload_size:
            data += client_screen.recv(4096)
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_screen.recv(4096)
        
        frame_data = data[:msg_size]
        # Giải mã dữ liệu ảnh
        with frame_lock:
            frame = pickle.loads(frame_data)
        
        # Nhận lệnh điều khiển từ người dùng server
        command = input("Nhập lệnh (click, move, type): ")
        client_control.send(command.encode('utf-8'))

finally:
    client_screen.close()
    client_control.close()
    cv2.destroyAllWindows()
