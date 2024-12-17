import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = urlopen("https://en.wikipedia.org/wiki/Python_(programming_language)")
    
    # BS4:
    bs = BeautifulSoup(url)
    # print(bs)

    for link in bs.find_all('a'):
        if 'href' in link.attrs:
            print(link.attrs['href'])

    # Find all images:
    cnt_img = 0
    for image in bs.find_all('img'):
        if 'src' in image.attrs:
            cnt_img += 1
            print(image)
    print(cnt_img)