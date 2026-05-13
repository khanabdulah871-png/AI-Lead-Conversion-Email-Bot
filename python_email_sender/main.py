import smtplib
import imaplib
import email as email_lib


#--------------------Email Sender--------------------#
# sender_email = input("SENDER EMAIL: ")
# receiver_email = input("RECEIVER EMAIL:")

# subject = input("SUBJECT: ")
# message = input("MESSAGE: ")

# text = f"Subject: {subject}\n\n{message}"

# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()

# server.login(sender_email, "lszc wmzo hxog ewjb")

# server.sendmail(sender_email, receiver_email, text)

# print("Email has been sent to " + receiver_email)



#--------------------Email Reader--------------------#
import imaplib
import email as email_lib

# Configuration
# add your email here
sender_email = 'rzi.codealigned@gmail.com' 
# The specific sender you want to filter
target_sender = "rzi.93.rzi@gmail.com" 

# add your app password here
password = "ufebprcmhpqohjca" 

print(f"\nChecking inbox for unseen emails from {target_sender}...\n")

try:
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(sender_email, password)
    imap.select("inbox")

    # Refactored Search: Combines UNSEEN and FROM criteria
    # The format is '(UNSEEN FROM "email@address.com")'
    search_criterion = f'(UNSEEN FROM "{target_sender}")'
    status, messages = imap.search(None, search_criterion)

    mail_ids = messages[0].split()

    if not mail_ids:
        print(f"Koi unread email nahi mili {target_sender} ki taraf se.")
    else:
        print(f"Total unread emails found: {len(mail_ids)}\n")

        # Process the emails
        for i in mail_ids:
            status, msg_data = imap.fetch(i, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email_lib.message_from_bytes(response_part[1])

                    subject = msg["subject"]
                    from_ = msg["from"]

                    print("From:", from_)
                    print("Subject:", subject)

                    # Email body extraction
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="replace")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="replace")
                    
                    print("Body:", body)

                    # Mark as Seen
                    imap.store(i, '+FLAGS', '\\Seen')
                    print("-" * 50)

    # Apply changes and close
    imap.expunge()
    imap.close()
    imap.logout()

except Exception as e:
    print(f"An error occurred: {e}")