import socket

def get_host_name_ip():
    try:
        hostname = socket.gethostname() # 'www.utc.edu.vn'
        hostip = socket.gethostbyname(hostname)

        print(f"Hostname: {hostname}")
        print(f"IP: {hostip}")

    except Exception as e:
        print("Cannot get IP")

if __name__ == '__main__':
    get_host_name_ip()