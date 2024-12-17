import socket
import struct
import pickle
import cv2
import pyautogui
import numpy as np

# Cấu hình client
SERVER_IP = '127.0.0.1'  # Đặt IP của server
PORT_SCREEN = 9999
PORT_CONTROL = 10000

# Tạo socket cho việc gửi màn hình
screen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen_socket.connect((SERVER_IP, PORT_SCREEN))

# Tạo socket để nhận lệnh điều khiển
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_socket.connect((SERVER_IP, PORT_CONTROL))

try:
    while True:
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Đóng gói và gửi ảnh
        data = pickle.dumps(frame)
        msg_size = struct.pack("L", len(data))
        screen_socket.sendall(msg_size + data)

        # Nhận lệnh từ server
        command = control_socket.recv(1024).decode('utf-8')
        if command.startswith("click"):
            pyautogui.click()
        
        elif command.startswith("move"):
            try:
                # Tách lấy x và y từ command
                x, y = map(int, command.split()[1:])
                pyautogui.moveTo(x, y)
            except ValueError:
                print("Lỗi: Lệnh 'move' không có tọa độ x, y hợp lệ.")
        
        elif command.startswith("type"):
            text = command.split(maxsplit=1)[1] if len(command.split()) > 1 else ""
            pyautogui.typewrite(text)
finally:
    screen_socket.close()
    control_socket.close()
