import getpass
import poplib
import pprint

GOOGLE_IMAP_SERVER = 'pop.googlemail.com'
POP_SERVER_PORT = 995

def check_email(username, password):
    mailbox = poplib.POP3_SSL(GOOGLE_IMAP_SERVER, POP_SERVER_PORT)

    mailbox.user(username)
    mailbox.pass_(password)

    num_message = len(mailbox.list()[1])

    print(f"Total: {num_message}")

    for msg in mailbox.retr(num_message):
        print(msg)

if __name__ == '__main__':
    username = input('Enter email account')
    password = getpass.getpass(prompt='Enter password: ')
    check_email(username, password)
