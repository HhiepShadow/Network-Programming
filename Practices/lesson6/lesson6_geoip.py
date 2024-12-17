from geoip import geolite2
import socket

# ipaddress la dia chi ip cua 1 host 
result = geolite2.lookup(ipaddress)

if result is not None:
    print(f"Country: {result.country}")
    print(f"{result.continent}")
    print(f"{result.timezone}")

import dnspython
dnspython.resolver # Phân giải tên miền -> địa chỉ IP

res = dnspython.resolver.query('www.abc.com', 'A')
for i in res:
    print(f'IP: {i.to_text()}')
    

