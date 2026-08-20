import smtplib
from email.message import EmailMessage

email = "netherlandsjobnotifs@gmail.com"
password = "vvdryxbvuqasaesm"

msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = email
msg["To"] = email

msg.set_content("If you received this, the email authentication works!")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(email, password)
    smtp.send_message(msg)

print("Success!")