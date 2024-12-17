from urllib import request

url = "https://httpbin.org/headers"
req = request.Request(url)
req.add_header("User-Agent", "Python-urllib/3.12")
response = request.urlopen(req)

print(response.read().decode("utf-8"))
