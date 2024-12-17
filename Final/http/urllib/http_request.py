from urllib import request

url = "https://www.youtube.com/watch?v=LwqBZy_YMWc"

response = request.urlopen(url)

print(response.read().decode("utf-8"))