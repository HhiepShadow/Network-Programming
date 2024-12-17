import requests
import threading
import time
import os

def get_weather_info(city_name, api_key, units='metric', stop_event=None):

    while not stop_event.is_set():
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={units}"
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP

            data = response.json()

            # Lấy thông tin: nhiệt độ, thời tiết, gió, mây, áp suất, độ ẩm
            main = data['main']
            weather = data['weather'][0]
            wind = data['wind']
            clouds = data['clouds']

            # Hiển thị thông tin thời tiết
            print(f"City: {city_name}")
            print(f"Temperature: {main['temp']}°C")  # alt + 0176: ký tự °
            print(f"Weather: {weather['description']}")
            print(f"Wind speed: {wind['speed']} m/s")
            print(f"Cloudiness: {clouds['all']}%")
            print(f"Pressure: {main['pressure']} hPa")
            print(f"Humidity: {main['humidity']}%")
            print("--------------------------------------------------")

            # Bộ đếm ngược 10 giây
            for i in range(10, 0, -1):
                print(f"Updating in {i} seconds...", end='\r')
                time.sleep(1)

            # Xóa màn hình
            os.system('cls')

        except requests.RequestException as e:
            print(f"Failed to get weather data for {city_name}. Error: {e}")

if __name__ == "__main__":
    api_key = 'c244f22c4cd4ee98867fe4830bca0176'
    city_name = 'Hanoi'
    #city_name = input("Enter city name: ")

    # Tạo sự kiện dừng
    stop_event = threading.Event()

    # Tạo và bắt đầu luồng
    weather_thread = threading.Thread(target=get_weather_info, args=(city_name, api_key, 'metric', stop_event))
    weather_thread.start()

    # Chờ người dùng nhấn Enter để dừng chương trình
    input("Press Enter to stop the program...\n")
    stop_event.set()
    weather_thread.join()