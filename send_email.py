import smtplib
import ssl
from email.message import EmailMessage
import getpass
import os

print("Welcome to Python Email Sender!")
sender_email = input("Enter your email address: ")
password = getpass.getpass("Enter your app password: ")  # hidden input
receiver_email = input("Enter receiver email address: ")
subject = input("Enter subject: ")

print("\nEnter your message (end with a blank line):")
lines = []
while True:
    line = input()
    if not line:
        break
    lines.append(line)
body = " ".join(lines)

attach_choice = input("\nDo you want to attach a file? (y/n): ").lower()
attachment_path = None

if attach_choice == 'y':
    attachment_path = input("Enter full path of file to attach: ")
    if not os.path.exists(attachment_path):
        print("File not found, skipping attachment.")
        attachment_path = None

# create email massages
msg = EmailMessage()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.set_content(body)

# Add attachment if provided
if attachment_path:
    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(f.name)
    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    print(f"📎 Attached file: {file_name}")

# connect to smtp server
smtp_server = "smtp.gmail.com"
port = 587  # for STARTTLS

context = ssl.create_default_context()

print("\n🔗 Connecting to SMTP server...")
try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # identify
        server.starttls(context=context)  # encrypt connection
        server.ehlo()
        server.login(sender_email, password)  # authenticate
        server.send_message(msg)  # send email
        print("\n✅ Email sent successfully!")

except smtplib.SMTPAuthenticationError:
    print("Authentication failed. Please check your email and app password.")
except smtplib.SMTPConnectError:
    print("Could not connect to the SMTP server.")
except Exception as e:
    print(f"Error: {e}")
