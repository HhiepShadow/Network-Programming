import socket
import cv2
import numpy as np
import struct

def main():
    server_ip = input("Enter the server IP address: ")
    server_port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        _, buffer = cv2.imencode(".jpg", frame)
        data = buffer.tobytes()
        msg_size = struct.pack("L", len(data))

        client_socket.sendall(msg_size + data)

        cv2.imshow('Webcam: ', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
