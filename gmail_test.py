# Gmail test

import os
import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv

load_dotenv()

# Access the secret key using the environment variable


SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


def send_message(body_text, recipient_email):
  
    # Set headers

    message = EmailMessage()
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email
    message["Subject"] = "Test Email with Python"
    message.set_content(body_text)

    print(message)

    context = ssl.create_default_context()

    # Send email using smtplib

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    try:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"An error occurred: {e}")
        
    #  Simulate sending functionality (replace with your actual sending logic)


send_message('test', 'martin.riveros@hotmail.com')