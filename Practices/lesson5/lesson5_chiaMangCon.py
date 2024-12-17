import ipaddress as ip

CLASS_C = '192.168.0.0'
prefix = 24             # 24-30

if __name__ == '__main__':
    net_addr = CLASS_C + "/" + str(prefix) 
    print(f"Network address: {net_addr}")

    try:
        network = ip.ip_network(net_addr)
    except:
        raise Exception("Fail to create network")
    
    print("Network configuration:")
    print(f"- Network address: {network.network_address}")
    print(f"- Number of IP addresses: {network.num_addresses}") # 2^8
    print(f"- Netmask: {network.netmask}")
    print(f"- Broadcast: {network.broadcast_address}")
    first_ip, last_ip = list(network.hosts())[0], list(network.hosts())[-1]

    print(f"- First IP address: {first_ip}")
    print(f"- Last IP address: {last_ip}")