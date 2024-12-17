import requests
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from mega import Mega


def download_file(url, filename):
    try:
        # Gửi yêu cầu GET đến URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Kiểm tra xem có lỗi không

        # Kiểm tra xem Content-Type có phải là ảnh không
        content_type = response.headers.get('Content-Type')
        if content_type is None or 'image' not in content_type:
            print(f"Warning: The URL does not point to an image. Content-Type: {content_type}")
            return
        
        # if not os.path.exists(folder):
        #     os.makedirs(folder)
        # file_path = os.path.join(folder, filename)

        # Mở tệp để ghi
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")



def download_file_from_mediafire(url):
    # Cấu hình trình duyệt (ví dụ dùng Chrome)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": r"D:\LearningDocument\Nam4-Ki1\LapTrinhMang\Code",  # Thay đổi đường dẫn lưu file tại đây
        "download.prompt_for_download": False,
    })
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Mở URL
        driver.get(url)
        
        # Chờ và nhấn nút tải xuống
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Download image"]'))
        ).click()
        
        time.sleep(5)
        
        # Đợi nút "Download file" xuất hiện và nhấn
        WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/download/")]'))
        ).click()
        
        print("Đang tải xuống tệp...")
        time.sleep(10)  # Chờ tải xuống hoàn tất
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    finally:
        print("Tải xuống thành công!!!")
        driver.quit()
        
def download_file_from_mega(url, filename):
    mega = Mega()
    
    # Đăng nhập ẩn danh
    m = mega.login()
    
    try:
        print("Đang tải xuống tệp từ MEGA.nz...")
        file = m.download_url(url, dest_filename=filename)  # Thay "downloaded_file" bằng tên tệp bạn muốn
        print(f"Tải xuống thành công: {file}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    # url = "https://a...content-available-to-author-only...e.vn/img/Iuvgc8KMYyJOgrLr-srTmx0rBlCLa5O3mRhQF0Fwlzk00NIzNsYT2t7BgSWRwtKx03Nim2b9JmsaBm9N/_DSC9432_1_l.jpg"  # Thay bằng URL của bạn
    # download_file(url, "image.jpg")    
    
    url = "https://w...content-available-to-author-only...e.com/view/wwi68v98zqhg3g7"  # Thay bằng URL của bạn
    download_file_from_mediafire(url)
    
    # url = "https://m...content-available-to-author-only...a.nz/file/TUdw3TBQ#-D9if4jKsYwJBncbk7tEELqmmJmi_eH8riopoPwx0dw"  # Thay bằng URL tệp MEGA của bạn
    # filename = "slide.docx"
    # download_file_from_mega(url, filename)

    