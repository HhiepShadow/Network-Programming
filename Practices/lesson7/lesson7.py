import ftplib
import os

def print_menu():
    print("\nMenu:")
    print("1. List directory")
    print("2. Change directory")
    print("3. Create directory")
    print("4. Delete file")
    print("5. Delete directory")
    print("6. Remane file or directory")
    print("7. Get file size")
    print("8. Download file")
    print("9. Upload file")
    print("10. Send custom command")
    print("11. Exit")

def list_directory(ftp):
    print("----------- Function List Directory -----------")
    try:
        files = []
        ftp.dir(files.append)
        return files
    
    except ftplib.all_errors as e:
        print(f"Error listing directory: {e}")
        return []

def change_directory(ftp, directory):
    print("----------- Function Change Directory -----------")
    try:
        ftp.cwd(directory)
        print(f"Changed to directory: {directory}")
    
    except ftplib.all_errors as e:
        print(f"Error create directory: {e}")

def create_directory(ftp, directory):
    print("----------- Function Create Directory -----------")
    try:
        ftp.mkd(directory)
        print(f"Created directory: {directory}")
    
    except ftplib.all_errors as e:
        print(f"Error creating directory: {e}")

def delete_file(ftp, filename):
    print("----------- Function Delete File -----------")
    try:
        ftp.delete(filename)
        print(f"Deleted file: {filename}")
    
    except ftplib.all_errors as e:
        print(f"Error deleting file: {e}")

def delete_directory(ftp, directory):
    print("----------- Function Delete Directory -----------")
    try:
        ftp.rmd(directory)
        print(f"Deleted directory: {directory}")
    
    except ftplib.all_errors as e:
        print(f"Error deleting directory: {e}")

def rename_file_or_directory(ftp, from_name, to_name):
    print("----------- Function Rename File or Directory -----------")
    try:
        ftp.rename(from_name, to_name)
        print(f"Renamed {from_name} to {to_name}")
    
    except ftplib.all_errors as e:
        print(f"Error renaming file or  directory: {e}")

def get_file_size(ftp, filename):
    print("----------- Function Get File size -----------")
    try:
        size = ftp.size(filename)
        print(f"File size: {size}")
    
    except ftplib.all_errors as e:
        print(f"Error get file size: {e}")

def download_file(ftp, file_orig, file_copy):
    print("----------- Function Download File -----------")
    try:
        with open(file_copy, "wb") as fp:
            ftp.retrbinary("RETR " + file_orig, fp.write)
            print(f"Download of {file_orig} to {file_copy} completed")
    except ftplib.all_errors as e:
        print(f"Error {e}")
        if os.path.isFile(file_copy):
            os.remove(file_copy)

def upload_file(ftp, file_name):
    print("----------- Function Upload file -----------")
    try:
        with open(file_name, "rb") as fp:
            response = ftp.storbinary("STOR " + file_name, fp)

            print(f"Server response: {response}")

            if not response.startswith("226"):
                print('Upload failed')
            else:
                print(f"Upload file {file_name} completed")
    except ftplib.all_errors as e:
        print(f"Error {e}")
        return []
    
def send_command(ftp, command):
    print("---------- Function send_command ----------")
    try:
        response = ftp.sendcmd(command)
        return response
    except ftplib.all_errors as e:
        print(f"Error sending command: {e}")
        return None

if __name__ == '__main__':
    with ftplib.FTP("127.0.0.1") as ftp:
        try:
            ftp.login("demo", "")
            ftp.set_pasv(True)

            print(ftp.getwelcome())

            while True:
                print_menu()
                choice = input("Enter your choice: ")
                # 1. Listing files in directory:
                if choice == "1":
                    entries = list_directory(ftp)
                    print(len(entries), " entries: ")
                    # print(list_directory(ftp))

                    for entry in entries:
                        print(entry)
                elif choice == "2":
                    directory = input("Enter your directory name you want to change: ")
                    change_directory(ftp, directory)

                elif choice == "3":
                    directory = input("Enter directory name you want to create: ")
                    create_directory(ftp, directory)

                elif choice == "4":
                    filename = input("Enter your file name you want to delete: ")
                    delete_file(ftp, filename)

                elif choice == "5":
                    directory = input("Enter your directory name you want to delete: ")
                    delete_directory(ftp, directory)

                elif choice == "6":
                    from_name = input("Enter your current name of file or directory you want to change: ")
                    to_name = input("Enter new name: ")
                    rename_file_or_directory(ftp, from_name, to_name)

                elif choice == "7":
                    filename = input("Enter your file name: ")
                    get_file_size(ftp, filename)

                elif choice == "8":
                    file_orig = input("Enter remote filename to download: ")
                    file_copy = input("Enter local path and filename to save as: ")
                    download_file(ftp, file_orig, file_copy)
                elif choice == "9":
                    filename = input("Enter local filename to upload: ")
                    upload_file(ftp, filename)
                elif choice == "10":
                    command = input("Enter custom FTP command: ")
                    response = send_command(ftp, command)
                    if response:
                        print(response)
                elif choice == "11":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            
        except ftplib.all_errors as e:
            print(f"FTP Errors: {e}")

