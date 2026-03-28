from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from bs4 import BeautifulSoup

def get_body(payload):
    body_data = None

    # Try to get plain text first
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body_data = part['body'].get('data')
                if body_data:
                    decoded = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    return decoded

        # If no plain text → fallback to HTML
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                body_data = part['body'].get('data')
                if body_data:
                    decoded = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    soup = BeautifulSoup(decoded, "html.parser")
                    return soup.get_text()

    else:
        body_data = payload['body'].get('data')
        if body_data:
            decoded = base64.urlsafe_b64decode(body_data).decode('utf-8')
            soup = BeautifulSoup(decoded, "html.parser")
            return soup.get_text()

    return ""

class GmailService:

    def __init__(self, access_token):
        self.access_token = access_token

    def get_unread_emails(self):
        # ✅ Create credentials using access token
        creds = Credentials(token=self.access_token)

        service = build("gmail", "v1", credentials=creds)

        results = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q="is:unread",
            maxResults=10
        ).execute()

        messages = results.get("messages", [])

        email_list = []

        for msg in messages:
            msg_id = msg["id"]

            msg_data = service.users().messages().get(
                userId="me",
                id=msg_id,
                format="full"
            ).execute()

            headers = msg_data["payload"]["headers"]

            subject = ""
            sender = ""

            for h in headers:
                if h["name"] == "Subject":
                    subject = h["value"]
                if h["name"] == "From":
                    sender = h["value"]

            email_list.append({
                "id": msg_id,
                "sender": sender,
                "subject": subject,
                "snippet": msg_data.get("snippet"),
                # "body": body,
                "date": msg_data.get("internalDate")
            })

        return email_list