# test_smtp.py
from email_utils import send_email

# Apni doosri email pe test karo
result = send_email(
    to_email = "khanabdulah871@gmail.com",  # yahan apni email likho
    subject  = "Test Email",
    body     = """
Hello,

This is a test email sent from our AI Sales Closer Agent.

Best regards,
Sales Team
    """
)

if result:
    print("Email successfuly sent!")
else:
    print("Email does not sent.")