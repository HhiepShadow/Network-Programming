import requests

# HTTP GET:
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.json())
print(response.status_code)

## HTTP POST:
data = {
    'title': 'foo',
    'body': 'bar',
    'userId': 1
}

response = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
print(response.status_code)
print(response.json())

## Params:
params = {
    'userId': 1
}
response = requests.get('https://jsonplaceholder.typicode.com/posts', params=params)
print(response.status_code)
print(response.content)