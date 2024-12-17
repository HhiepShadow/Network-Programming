from urllib import request, parse

base_url = 'https://httpbin.org/get'
params = {
    'search': 'python',
    'page': 2
}
url_with_params = f"{base_url}?{parse.urlencode(params)}"
response = request.urlopen(url_with_params)
print(response.read().decode('utf-8'))
