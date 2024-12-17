import socket

host = "127.0.0.1"
ip_addr = socket.gethostbyname(host)

# Quét các cổng
while 1:
    port_number = int(input("Enter port: "))
    try:
        s = socket.socket()
        request = s.connect((ip_addr, port_number))
        print(f"Port {port_number} open")
        s.close()
    except socket.error as e:
        print(f"Port {port_number} close")
        