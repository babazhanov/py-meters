

server = 'mg-exch.mg.metinvest.com'

DOMAIN = 'mg'
USER = 'r.babazhanov'
PASS = '9ijn*UHB'


import imaplib
import email
import email.message
from datetime import datetime


class MailBox():
    
    def __init__(self):
        self.__imap = imaplib.IMAP4_SSL(server)
        self.__imap.login(USER, PASS)

    def __del__(self):
        #self.__imap.close()
        self.__imap.logout()
    
    def get_num(self):
        
        inbox = self.__imap.select('INBOX')
        num = -1
        if isinstance(inbox, tuple) and inbox[0] == 'OK':
            num = int(inbox[1][0])

        return num

    def get_headers_lastn(self, lastn):
        headers = []

        inbox = self.__imap.select('INBOX')
        ids = self.__imap.search(None, 'ALL')
        if isinstance(ids, tuple) and ids[0] == 'OK':
            ids = ids[1][0]
            ids = ids.split(b' ')
            
            for id_ in ids[-lastn:]:
                status, data =  self.__imap.fetch(id_, '(RFC822)')

                if status == 'OK':
                    msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage)
                    subject = email.header.decode_header(msg['subject'])
                    subject = str(email.header.make_header(subject))

                    from_ = email.header.decode_header(msg['from'])
                    # parseaddr
                    from_ = str(email.header.make_header(from_))                    

                    date = email.utils.parsedate_tz(msg['Date'])
                    date = datetime(*date[:6]).strftime("%d.%m.%Y %H:%M:%S")

                    headers.append((subject, from_, date))

        return headers

if __name__ == "__main__":
    M = MailBox()
    
    print(M.get_num())
    print(M.get_headers_lastn(15))
