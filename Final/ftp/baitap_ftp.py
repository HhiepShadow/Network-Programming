import ftplib
import os

def list_directory(ftp: ftplib.FTP):
    try:
        files = ftp.retrlines("LIST")
        return files
    except ftplib.all_errors as e:
        print(f"Error: {e}")
        return []
        
def change_directory(ftp: ftplib.FTP, directory):
    try:
        ftp.cwd(directory)
        print(f"Changed to directory: {directory}")
    except ftplib.all_errors as e:
        print(f"Error changing directory: {e}")
    
def create_directory(ftp: ftplib.FTP, directory_name):
    try:
        ftp.mkd(directory_name)
        print(f"Created directory: {directory_name}")
    except ftplib.all_errors as e:
        print(f"Error creating directory: {directory_name}")
    
def delete_file(ftp: ftplib.FTP, filename):
    try:
        ftp.delete(filename)
        print(f"Deleted filename: {filename}")
    except ftplib.all_errors as e:
        print(f"Error deleting filename: {filename}")

def delete_directory(ftp: ftplib.FTP, directory_name):
    try:
        ftp.rmd(directory_name)
        print(f"Deleted directory: {directory_name}")
    except ftplib.all_errors as e:
        print(f"Error deleting directory {directory_name}")
    
def rename_file_or_directory(ftp: ftplib.FTP, from_name, to_name):
    try:
        ftp.rename(from_name, to_name)
        print(f"Renamed {from_name} to {to_name}")
    except ftplib.all_errors as e:
        print(f"Error renaming: {e}")

def get_file_size(ftp: ftplib.FTP, filename):
    try: 
        size = ftp.size(filename)
        print(f"Size of {filename}: {size}")
        return size
    except ftplib.all_errors as e:
        print(f"Error getting file size: {e}")

def download_file(ftp: ftplib.FTP, filename, file_copy):
    try:
        with open(file_copy, "wb") as fc:
            ftp.retrbinary(f"RETR {filename}", fc.write)
        print(f"Downloaded {filename}")
    except ftplib.all_errors as e:
        print(f"Error downloading file {filename}")
    
def upload_file(ftp: ftplib.FTP, filename):
    try:
        with open(filename, "rb") as fu:
            response = ftp.storbinary(f"STOR {filename}", fu)
            print(f"Server response: {response}")
            if response.startswith("226"):
                print(f"Uploaded file {filename}")        
            else:
                print("Uploaded failed")
    except ftplib.all_errors as e:
        print(f"Error uploading file: {e}")

def send_custom_command(ftp: ftplib.FTP, cmd):
    try:
        response = ftp.sendcmd(cmd)
        return response
    except ftplib.all_errors as e:
        print(f"Error sending command: {e}")

def print_menu():
    print("\nMenu:")
    print("1. List directory")
    print("2. Change directory")
    print("3. Create directory")
    print("4. Delete file")
    print("5. Delete directory")
    print("6. Rename file or directory")
    print("7. Get file size")
    print("8. Download file")
    print("9. Upload file")
    print("10. Send custom command")
    print("11. Exit")

if __name__ == "__main__":
    ftp = ftplib.FTP(host="127.0.0.1")
    try:
        ftp.login("demo", "")
        ftp.set_pasv(True)
        while True:
            print_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                files = list_directory(ftp)
                print(files)
    except ftplib.all_errors as e:
        print(f"Error: {e}")            
