import ipaddress

ip = input("Enter your IP address: ")
try:
    network = ipaddress.ip_network(ip)
    print(f"Network address: {network.network_address}")
    print(f"Broadcast address: {network.broadcast_address}")
    print(f"Subnet mask: {network.netmask}")
    print(f"Number of vailable hosts: {network.num_addresses - 2}")
except ValueError:
    print(f"{ip} is not an valid address")