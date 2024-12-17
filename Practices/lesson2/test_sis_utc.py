import requests
from bs4 import BeautifulSoup
import pandas as pd
import getpass

# with open('file.txt', 'rb') as file:
#     file = {'file': file}
#     response = requests.post('https://www.example.com', files=file)
#     print(response.status_code)
#     print(response.text)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# link = "https://sis.utc.edu.vn/index.php"
link = "https://sis.utc.edu.vn/survey/overview.php"
# url = "http://sis.utc.edu.vn/"

username = input("username: ")
password = getpass.getpass(prompt="Password: ")

data = {
    'username': username,
    'password': password
}

res = requests.post(link, data=data, headers=headers)

if res.status_code == 200:
    print('Successful login')
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        print(soup.prettify())
        print(soup)

        table = soup.find("table", {"class": "list"})

        if table:
        # Tìm tất cả các thẻ <a> với class là "hashchange"
            columns = [a.text.strip() for a in table.find_all("a", {"class": "hashchange"})]

            # Nếu không tìm thấy cột nào, sử dụng thẻ <th> để lấy tên cột
            if not columns:
                columns = [th.text.strip() for th in table.find_all("th")]

            data_text = []
            for row in table.find_all("tr"):
                data_row = [col.text.strip() for col in row.find_all("td")]
                if data_row:
                    data_text.append(data_row)

            df = pd.DataFrame(data_text, columns=columns)

            df.to_excel('data.xlsx', index=False)
        else:
            print("Table not found")
    else:
        print("Bad Request")
else:
    print("Login failed")


