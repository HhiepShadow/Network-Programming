import requests

def get_geo_info(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        geo_info = response.json()

        print(f"HTTP status: {str(response.status_code)}")
        print(f"Headers Responses: {response.headers}")
        print("List of header items: ")
        for header in response.headers.items():
            print(header)

        print(f"Headers Requests: {response.request.headers}")
        for header, value in response.request.headers.items():
            print(header + " --> " + value)

        print(geo_info)
        # print(f"IP address: {geo_info.get('ip')}")
        # print(f"Country: {geo_info.get("country_name")}")
        # print(f"Region: {geo_info.get('region_name')}")
        # print(f"City: {geo_info.get('city')}")
        # print(f"ZIP code: {geo_info.get('zipcode')}")
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    url = f'https://ipinfo.io/59.153.248.64/json'
    get_geo_info(url)