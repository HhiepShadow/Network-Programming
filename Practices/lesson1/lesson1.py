from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.request import Request
import gzip

try:
    request = Request("https://www.utc.edu.vn")

    # Header:
    request.add_header("Accept-Language", "en")

    # Encoding:
    request.add_header("Accept-Encoding", "gzip")

    response = urlopen(request)

    result = response.read()

    decoded = gzip.decompress(result)
    
    print(response.url)
    print(response.status)
    # print(response.read())
    print(response.getheaders())
    print(result)
except HTTPError as e:
    print(e)

