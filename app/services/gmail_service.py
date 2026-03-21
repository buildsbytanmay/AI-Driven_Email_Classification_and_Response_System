from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

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
                id=msg_id
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
                "date": msg_data.get("internalDate")
            })

        return email_list