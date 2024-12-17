import socket
import cv2
import numpy as np
import struct

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on port {port}")

    client_socket, client_addr = server_socket.accept()

    print(f"Connection from {client_addr}")

    data = b""
    payload_size = struct.calcsize("L")

    while True:
        while len(data) < payload_size:
            data += client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        if frame is not None and frame.size > 0:
            cv2.imshow("Server", frame)
        else:
            print("Lỗi: Ảnh không hợp lệ hoặc không thể giải mã.")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    start_server()

