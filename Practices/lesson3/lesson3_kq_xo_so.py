from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re 

if __name__ == '__main__':
    url = 'https://www.kqxs.vn/mien-bac'

    headers = requests.utils.default_headers()

    r = requests.get(url, headers)

    bs = BeautifulSoup(r.content, 'html.parser')

    images = bs.find_all('img')

    count_images = 0
    for image in images:
        count_images += 1
        print(image.attrs['src'])
    print(count_images)
