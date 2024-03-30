import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

def welcome_new_user(to_email, from_email=os.environ["EMAIL_SENDER"], from_password=os.environ["EMAIL_PASSWORD"]):
    base_url = os.environ["BASE_URL"]
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Invitation to join Modtools Image"

    html_body = f"""
    <html>
        <body>
            <h2>You are invited to join Modtools Image!</h2>
            <p>Click <a href="{base_url}/register">here</a> to register for an account!</p>
            <p>Best regards,</p>
            <p>The Modtools Image Team</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))
    try: 
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        print("Email sent!")
    except Exception as e:
        print(f"Something went wrong... {e}")


def email_action(to_email,metadata):
    from_email=os.environ["EMAIL_SENDER"]
    from_password=os.environ["EMAIL_PASSWORD"]
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Image action needed"

    html_body = """
    <html>
        <body>
            <p>A new image submited with following metadata</p>
            <p>{}</p>
            <p>The CSAM filtering Team</p>
        </body>
    </html>
    """.format(str(metadata))

    msg.attach(MIMEText(html_body, 'html'))
    try: 
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        print("Email sent!")
    except Exception as e:
        print(f"Something went wrong... {e}")
