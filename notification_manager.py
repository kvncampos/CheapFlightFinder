import json
import smtplib, ssl
import os
from Cell_Providers import providers
# used for MMS
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from wrapper import time_function


class NotificationSender:

    def __init__(self):
        self.number = os.environ.get('CELL_NUMBER', 'CellNumber Not SET as ENV Variable.')
        self.provider = os.environ.get('PROVIDER', 'Provider Not SET as ENV Variable.')
        self.sender_credentials = (
            os.environ.get('GMAIL', 'GMAIL Not SET as ENV Variable.'),
            os.environ.get('GMAIL_APP_PASS', 'GMAIL PASS Not SET as ENV Variable.')
        )
        self.subject = "FlightApp Trigger"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465

    @time_function
    def send_sms_via_email(self, message: str):
        sender_email, email_password = self.sender_credentials
        receiver_email = f'{self.number}@{providers.get(self.provider).get("sms")}'

        email_message = f"Subject:{self.subject}\nTo:{receiver_email}\n{message}"

        with smtplib.SMTP_SSL(
                self.smtp_server, self.smtp_port, context=ssl.create_default_context()
        ) as email:
            email.login(sender_email, email_password)
            email.sendmail(sender_email, receiver_email, email_message)

    @time_function
    def send_mms_via_email(self,
                           message: str,
                           file_path: str,
                           mime_maintype: str,
                           mime_subtype: str,
                           ):
        sender_email, email_password = self.sender_credentials
        receiver_email = f'{self.number}@{providers.get(self.provider).get("sms")}'

        email_message = MIMEMultipart()
        email_message["Subject"] = self.subject
        email_message["From"] = sender_email
        email_message["To"] = receiver_email

        email_message.attach(MIMEText(message, "plain"))

        with open(file_path, "rb") as attachment:
            part = MIMEBase(mime_maintype, mime_subtype)
            part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={basename(file_path)}",
            )

            email_message.attach(part)

        text = email_message.as_string()

        with smtplib.SMTP_SSL(
                self.smtp_server, self.smtp_port, context=ssl.create_default_context()
        ) as email:
            email.login(sender_email, email_password)
            email.sendmail(sender_email, receiver_email, text)

    @time_function
    def send_email(self, body: str):
        sender_email = os.environ.get('GMAIL', 'GMAIL Not SET as ENV Variable.')
        email_password = os.environ.get('GMAIL_APP_PASS', 'GMAIL PASS Not SET as ENV Variable.')

        msg = MIMEText(body, 'html')
        msg['Subject'] = self.subject
        msg['From'] = sender_email
        msg['To'] = sender_email
        # msg.attach(body_message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, email_password)
            smtp_server.sendmail(sender_email, sender_email, msg.as_string())

        print("Message sent!")

    @time_function
    def send_email_to_all(self, body: str, email_file):
        sender_email = os.environ.get('GMAIL', 'GMAIL Not SET as ENV Variable.')
        email_password = os.environ.get('GMAIL_APP_PASS', 'GMAIL PASS Not SET as ENV Variable.')
        with open(email_file, 'r') as emails:
            user_emails = json.loads(emails.read())

        for sub in user_emails.keys():
            msg = MIMEText(body, 'html')
            msg['Subject'] = self.subject
            msg['From'] = sender_email
            msg['To'] = sub
            # msg.attach(body_message)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender_email, email_password)
                smtp_server.sendmail(sender_email, sender_email, msg.as_string())

            print("Message sent!")

    def main(self):
        message = "hello world! Ran Directly from notifications_manager.py"

        # Send Email
        self.send_email(body=message)

        # SMS
        # self.send_sms_via_email(message)

        # # MMS
        file_path = "/path/to/file/file.png"

        mime_maintype = "image"
        mime_subtype = "png"

        self.send_mms_via_email(
            message,
            file_path,
            mime_maintype,
            mime_subtype,
        )


if __name__ == "__main__":
    test = NotificationSender()
    test.main()
