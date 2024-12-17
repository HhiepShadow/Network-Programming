import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_data_weather_forcast():
    url = 'https://forecast.weather.gov/MapClick.php?lat=40.7130466&lon=-74.0072301'
    headers = requests.utils.default_headers()
    response = requests.get(url, headers)
    bs = BeautifulSoup(response.content, 'html.parser')
    
    week = bs.find(id = 'seven-day-forecast')
    w = week.find_all(class_ = 'tombstone-container')
    d = []
    for i in range(len(w) - 1):
        period = w[i].find(class_ = 'period-name').get_text()
        short_decs = w[i].find(class_ = 'short-desc').get_text()
        temp = w[i].find(class_ = 'temp').get_text()
        img = w[i].find('img')['title']
        d.append((period, short_decs, temp, img))
    
    for i in range(len(d) - 1):
        print(d[i])

if __name__ == "__main__":
    get_data_weather_forcast()
    pass