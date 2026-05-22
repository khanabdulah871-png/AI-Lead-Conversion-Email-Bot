# # email_utils.py
# import imaplib
# import email
# from email.header import decode_header
# import config

# def connect_imap():
#     mail = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
#     mail.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
#     return mail

# def decode_str(value):
#     if value is None:
#         return ""
#     decoded, encoding = decode_header(value)[0]
#     if isinstance(decoded, bytes):
#         return decoded.decode(encoding or "utf-8", errors="ignore")
#     return decoded

# def fetch_unread_emails():
#     mail = connect_imap()
#     mail.select("inbox")

#     # Sirf unread emails fetch karo
#     _, message_ids = mail.search(None, "UNSEEN")
#     email_list = []

#     for msg_id in message_ids[0].split():
#         _, msg_data = mail.fetch(msg_id, "(RFC822)")
#         raw_email = msg_data[0][1]
#         msg = email.message_from_bytes(raw_email)

#         # Subject, sender, body extract karo
#         subject = decode_str(msg.get("Subject"))
#         sender  = decode_str(msg.get("From"))
#         body    = ""

#         if msg.is_multipart():
#             for part in msg.walk():
#                 if part.get_content_type() == "text/plain":
#                     body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
#                     break
#         else:
#             body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

#         email_list.append({
#             "id"     : msg_id.decode(),
#             "sender" : sender,
#             "subject": subject,
#             "body"   : body.strip()
#         })

#     mail.logout()
#     return email_list





# email_utils.py
import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

# ─────────────────────────────────────────
# IMAP — Email padhna
# ─────────────────────────────────────────
def connect_imap():
    mail = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
    mail.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    return mail

def decode_str(value):
    if value is None:
        return ""
    decoded, encoding = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8", errors="ignore")
    return decoded

def fetch_unread_emails():
    mail = connect_imap()
    mail.select("inbox")

    _, message_ids = mail.search(None, "UNSEEN")
    email_list = []

    for msg_id in message_ids[0].split():
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = decode_str(msg.get("Subject"))
        sender  = decode_str(msg.get("From"))
        body    = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        email_list.append({
            "id"     : msg_id.decode(),
            "sender" : sender,
            "subject": subject,
            "body"   : body.strip()
        })

    mail.logout()
    return email_list


# ─────────────────────────────────────────
# SMTP — Email bhejna
# ─────────────────────────────────────────
def connect_smtp():
    smtp = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    smtp.starttls()
    smtp.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    return smtp

def send_email(to_email, subject, body):
    try:
        # Email message banao
        msg = MIMEMultipart()
        msg["From"]    = config.EMAIL_ADDRESS
        msg["To"]      = to_email
        msg["Subject"] = f"Re: {subject}"

        # Body attach karo
        msg.attach(MIMEText(body, "plain"))

        # Send karo
        smtp = connect_smtp()
        smtp.sendmail(config.EMAIL_ADDRESS, to_email, msg.as_string())
        smtp.quit()

        # time.sleep(2)

        print(f"Email sent to: {to_email}")
        return True

    except Exception as e:
        print(f"Email send nahi hui: {e}")
        return False