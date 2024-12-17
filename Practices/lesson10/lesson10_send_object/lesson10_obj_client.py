import socket

class SV:
    def __init__(self, maSV, hoTen, diemTB):
        self.maSV = maSV
        self.hoTen = hoTen
        self.diemTB = diemTB

    def __str__(self):
        return str(self.maSV) + " - " + self.hoTen + " - " + str(self.diemTB)


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
            # command = input("Enter command or message to send to server: ")

            maSV = int(input("Ma sv: "))
            hoTen = input("Ho ten: ")
            diemTB = float(input("Diem TB"))
            sv = SV(maSV=maSV, hoTen=hoTen, diemTB=diemTB)
            message = str(sv)
            s.send(message.encode("utf-8"))

    except socket.error as e:
        print("Error: ", e)
    finally:
        s.close()
