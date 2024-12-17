import ipaddress as ip
from sys import prefix

CLASS_C = "192.168.0.0"
prefix = 24

if __name__ == "__main__":
    net_addr = f"{CLASS_C}/{prefix}"
    print(f"network address: {net_addr}")
    try:
        network = ip.ip_network(net_addr)
    except:
        raise Exception("Fail to create network!")
    print("network configuration")
    print(f"\tnetwork address: {network.network_address}")
    print(f"\tnumber of IP address: {network.num_addresses}")
    print(f"\tsubnet mask: {network.netmask}")
    print(f"\tbroadcast: {network.broadcast_address}")
    list_ip = list(network.hosts())
    print(f"\tfirst IP: {list_ip[0]}")
    print(f"\tlast IP: {list_ip[-1]}")

    i = 0
    for subnet in network.subnets(new_prefix=27):
        print(f"{i}. Subnet: {subnet}")
        print(f"    first IP: {subnet[0]}")
        print(f"    last IP: {subnet[-1]}")
        i += 1