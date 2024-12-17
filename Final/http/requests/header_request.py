import requests

url = 'https://httpbin.org/headers'
headers = {
    'Authorization': 'Bearer'
}

response = requests.get(url, headers=headers)
print(response.json())