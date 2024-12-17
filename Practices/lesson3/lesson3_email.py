import requests
# from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def extract_email(url):
    try:
        headers = requests.utils.default_headers()

        response = requests.get(url, headers)
        response.raise_for_status()

        data = response.text 

        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-].[a-zA-Z]{2,}'

        emails = re.findall(email_pattern, data)

        # Filter duplicated emails:
        filtered_emails = set(emails)

        return filtered_emails
    except requests.RequestException as e:
        print(f"Error: {e}")
        return set()

if __name__ == '__main__':
    url = 'https://cellphones.com.vn/'
    emails = extract_email(url)    
    for email in emails:
        print(email)