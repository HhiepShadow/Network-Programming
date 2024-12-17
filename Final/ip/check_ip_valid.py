import ipaddress

ip = input("Enter your IP address: ")
try:
    ip_obj = ipaddress.ip_address(ip)
    print(f"{ip} is an valid IP address")
except ValueError:
    print(f"{ip} is an invalid IP address")