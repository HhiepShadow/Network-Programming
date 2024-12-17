import requests

url = 'https://httpbin.org/post'
files = {
    'file': open('example.txt', 'rb')
}

response = requests.post(url, files=files)
print(response.json())