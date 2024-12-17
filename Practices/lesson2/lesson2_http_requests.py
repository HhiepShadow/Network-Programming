import urllib.request
import requests
import urllib

if __name__ == '__main__':
    data = {
        'userId': 1,
        'id': 101,
        'title': 'Hello World',
        'body': 'Test input'
    }

    req = urllib.request.Request('https://jsonplaceholder.typicode.com/posts')
    res = urllib.request.urlopen(req)
    print()
    

    url = "https://jsonplaceholder.typicode.com/posts"

    url2 = "https://api.github.com"
    response = requests.post(url=url, json=data)

    # print("Status code: ", response.status_code)
    # print("Body: ", response.text)

    response_get = requests.get(url=url+'/1')

    # Trả về status
    print(response_get)

    # Lấy dưới dạng JSON:
    print(response_get.json())
