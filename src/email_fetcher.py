from database import Database
from imaplib import IMAP4_SSL
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

class EmailFetcher:
    def __init__(self):
        load_dotenv()
        self.db = Database()
        # self.email = os.getenv('EMAIL_ADDRESS')
        # self.password = os.getenv('EMAIL_PASSWORD')
        # self.imap_server = os.getenv('IMAP_SERVER')

    async def fetch_recent_emails(self, limit=10):
        accounts = self.db.get_active_accounts()
        all_emails = []
        for account in accounts:
            account_config = {
                'email': account[1],
                'password': account[2], 
                'imap_server': account[3]
            }
            account_emails = await self._fetch_account_emails(account_config, limit)
            all_emails.extend(account_emails)
        return all_emails
    async def _fetch_account_emails(self, account, limit):
         with IMAP4_SSL(account['imap_server']) as imap:
            imap.login(account['email'], account['password'])
            # imap.login(self.email, self.password)
            imap.select('INBOX')
            
            _, messages = imap.search(None, 'ALL')
            email_ids = messages[0].split()
            print(f"Total emails found: {len(email_ids)}")
            
            emails = []
            for email_id in email_ids[-limit:]:
                _, msg_data = imap.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                message = email.message_from_bytes(email_body)
                
                content = self._get_email_content(message)
                emails.append({
                    'subject': decode_header(message['subject'])[0][0],
                    'from': message['from'],
                    'date': message['date'],
                    'content': content,
                    'source_account': account['email']
                })
            print(f"Fetched emails: {[e['subject'] for e in emails]}") 
            return emails

    def _get_email_content(self, message):
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return message.get_payload(decode=True).decode()