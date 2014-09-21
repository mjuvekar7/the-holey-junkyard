import imaplib
import getpass as gp

uname = raw_input('Enter username (Gmail): ')
passwd = gp.getpass('Enter password: ')

# setup and login
imap_server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap_server.login(uname, passwd)

imap_server.select('INBOX')

# print no. of unread emails
status, response = imap_server.status('INBOX', "(UNSEEN)")
# print(response)
unreadcount = int(response[0].split()[2].strip(').,]'))
print(unreadcount)
