import urllib
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
import datetime
# HTTP Requests Method:
import requests


if __name__ == '__main__':
    req = Request('http://www.python.org')
    open = urlopen(req)

    print(req.redirect_dict)
    print(open.url)

    print(open.getheader('User-agent'))

    # Cookies:
    cookie_jar = CookieJar()
    http_opener = build_opener(HTTPCookieProcessor(cookie_jar))

    req_2 = http_opener.open('http://www.github.com')
    print(req_2)

    print(len(cookie_jar))

    cookies = list(cookie_jar)

    print(cookies[0].name)
    print(cookies[0].value)
    print(cookies[0].domain)
    print(cookies[0].path)
    print(cookies[0].expires)
    print(cookies[0].secure)
    for c in cookies:
        print(c)

    # Datetime Linux:
    print(datetime.datetime.fromtimestamp(cookies[1].expires))

    # Download:
    print("Starting downloading ...")
    url = "https://www.python.org/static/img/python-logo.png"
    urllib.request.urlretrieve(url, 'python.png')
    with urllib.request.urlopen(url) as r:
        print('Status: ', r.status)
        print('Downloading python.org...')
        with open('python.org', 'wb') as image:
            image.write(r.read())