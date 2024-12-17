import getpass
import imaplib
import pprint

GOOGLE_IMAP_SERVER = 'imap.googlemail.com' # 'imap.gmail.com:993'
IMAP_SERVER_PORT = 993

def check_email(username, password):
    mailbox = imaplib.IMAP4_SSL(GOOGLE_IMAP_SERVER, IMAP_SERVER_PORT)
    mailbox.login(username, password)
    mailbox.select('Inbox')
    tmp, data = mailbox.search(None, 'ALL')

    # data là 1 danh sách các email
    for num in data[0].split():
        tmp, data = mailbox.fetch(num, 'RFC822')
        print(f'Email: {num}')
        pprint.pprint(data[0][1])
    
    mailbox.close()
    mailbox.logout()

if __name__ == '__main__':
    username = input('Enter email account')
    password = getpass.getpass(prompt='Enter password: ')
    check_email(username, password)
