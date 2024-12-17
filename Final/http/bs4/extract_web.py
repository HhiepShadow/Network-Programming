import requests
import bs4

url = 'https://www.kqxs.vn/mien-bac'
headers = requests.utils.default_headers()

response = requests.get(url, headers)

soup = bs4.BeautifulSoup(response.content, 'html.parser')

# imgs = soup.find_all('img')
# print(len(imgs))
# for img in imgs:
#     print(img.get('src'))

divs = soup.find_all('div', class_='')
print(len(divs))
for div in divs:
    print(div)
