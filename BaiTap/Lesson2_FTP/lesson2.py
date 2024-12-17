from ftplib import FTP
import ftplib

class FTPClient:
    def __init__(self, host, username, password):
        self.ftp = FTP(host)
        self.ftp.login(username, password)
        print("Login successfully")
    
    def list_files(self):
        return self.ftp.nlst()
    
    def download_file(self, filename):
        try:
            with open(filename, 'wb') as f:
                self.ftp.retrbinary(f"RETR {filename}", f.write)
                print(f"Downloaded: {filename}")
        except ftplib.all_errors as e:
            print(f"FTP errors: {e}")

    def upload_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.ftp.storbinary(F"STOR {filename}", f)
                print(f"Uploaded {filename}")
        except ftplib.all_errors as e:
            print(f"FTP errors: {e}")
    
    def rename_file(self, old_name, new_name):
        try:
            self.ftp.rename(old_name, new_name)
            print(f"Renamed from {old_name} to {new_name}")
        except ftplib.all_errors as e:
            print(f"FTP errors: {e}")
    
    def delete_file(self, filename):
        try:
            self.ftp.delete(filename)
            print(f"Deleted {filename}")
        except ftplib.all_errors as e:
            print(f"FTP errors: {e}")

    def create_directory(self, dirname):
        try:
            self.ftp.mkd(dirname)
            print(f"Created directory: {dirname}")
        except ftplib.all_errors as e:
            print(f"FTP errors: {e}")

    def quit(self):
        self.ftp.quit()

def main():
    host = input("Enter FTP server address: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    ftp = FTPClient(host, username, password)
    print("Logged in successfully!")

    while True:
        print("\nOptions:")
        print("1. List files")
        print("2. Download a file")
        print("3. Upload a file")
        print("4. Rename a file")
        print("5. Delete a file")
        print("6. Create a directory")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            files = ftp.list_files()
            print("Files on server:")
            for file in files:
                print(file)

        elif choice == '2':
            filename = input("Enter filename to download: ")
            ftp.download_file(filename)

        elif choice == '3':
            filename = input("Enter filename to upload: ")
            ftp.upload_file(filename)

        elif choice == '4':
            old_name = input("Enter current filename: ")
            new_name = input("Enter new filename: ")
            ftp.rename_file(old_name, new_name)

        elif choice == '5':
            filename = input("Enter filename to delete: ")
            ftp.delete_file(filename)

        elif choice == '6':
            dirname = input("Enter directory name to create: ")
            ftp.create_directory(dirname)

        elif choice == '7':
            ftp.quit()
            print("Logged out.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()