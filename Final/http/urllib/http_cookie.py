from urllib import request
from http.cookiejar import CookieJar, Cookie

cookieJar = CookieJar()
handler = request.HTTPCookieProcessor(cookieJar)
opener = request.build_opener(handler)

url = 'https://httpbin.org/cookies/set?name=value'
opener.open(url)

for ck in cookieJar:
    print(ck.name + " - " + ck.value)