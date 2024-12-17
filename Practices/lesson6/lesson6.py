import netifaces

def get_interface():
    interfaces = netifaces.interfaces()

    my_interfaces = dict()

    for i in interfaces:
        addr = netifaces.ifaddresses(i)
        my_addr = dict()

        # IPv4 family:
        if netifaces.AF_INET in addr.keys():
            my_addr['ipv4'] = addr[netifaces.AF_INET]
        
        # IPv6 family:
        if netifaces.AF_INET6 in addr.keys():
            my_addr['ipv6'] = addr[netifaces.AF_INET6]
        
        my_interfaces[i] = my_addr
    
    return my_interfaces

def get_broadcast_addr():
    broadcast_addr = list()
    for i in netifaces.interfaces():
        ifaddresses = netifaces.ifaddresses(i)

        for addr_family in ifaddresses:
            if addr_family == netifaces.AF_INET:
                addr_info = ifaddresses[addr_family]
                
                for info in addr_info:
                    if 'broadcast' in info:
                        broadcast_addr.append(info['broadcast'])
    
    return broadcast_addr


if __name__ == '__main__':
    my_interfaces = get_interface()
    print(my_interfaces)

    my_broadcast = get_broadcast_addr()
    print(my_broadcast)