# test_imap.py
from email_utils import fetch_unread_emails

emails = fetch_unread_emails()

if not emails:
    print("Koi unread email nahi mili.")
else:
    for e in emails:
        print("---")
        print("From   :", e["sender"])
        print("Subject:", e["subject"])
        print("Body   :", e["body"][:200])