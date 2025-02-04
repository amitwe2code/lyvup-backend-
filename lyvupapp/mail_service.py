from mailersend import emails
from django.conf import settings
from mailersend import email_verification
from dotenv import load_dotenv
import os
import requests
from rest_framework.response import Response

# from mailersend import emails
# from django.conf import settings
# from dotenv import load_dotenv
# import os

class MailerSendService:
    load_dotenv()
    MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')
    def forget_mail(self,data):
        email = data.get('email')
        url = data.get('url')

        print('mailer send in forget',email)
        self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
        mail_body={}
        mail_from = {
            "name": "lyvup",
            "email": 'MS_lTm1Jr@trial-3zxk54veprqljy6v.mlsender.net',
        }

        recipients = [
            {
                "name": "Your Client",
                "email":email,
            }
        ]

        reply_to = {
            "name": "Name",
            "email": "amitpatidar.we2code@gmail.com",
        }
        self.mailer.set_mail_from(mail_from, mail_body)
        self.mailer.set_mail_to(recipients, mail_body)
        self.mailer.set_subject("forget password", mail_body)
        self.mailer.set_html_content(f"<h1>forget password</h1><br/><p>forget password url {url}</p>", mail_body)
        # self.mailer.set_template("vywj2lp692q47oqz", mail_body)
        # self.mailer.set_plaintext_content("This is the text content", mail_body)
        self.mailer.set_reply_to(reply_to, mail_body)
        self.mailer.send(mail_body)
        print ('send success full')
        return Response({
            'status_code':202,
        })


    def send_email(self): 
        print('mailer chalne ke pehle ')
        self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
        mail_body={}
        mail_from = {
            "name": "lyvup",
            "email": 'MS_lTm1Jr@trial-3zxk54veprqljy6v.mlsender.net',
        }

        recipients = [
            {
                "name": "Your Client",
                "email": 'amitpatidar.we2code@gmail.com',
            }
        ]

        reply_to = {
            "name": "Name",
            "email": "amitpatidar.we2code@gmail.com",
        }

        self.mailer.set_mail_from(mail_from, mail_body)
        self.mailer.set_mail_to(recipients, mail_body)
        self.mailer.set_subject("Login Success", mail_body)
        self.mailer.set_html_content("<h1>login success</h1><br/><p>login success now you can perform your task</p>", mail_body)
        # self.mailer.set_template("vywj2lp692q47oqz", mail_body)
        # self.mailer.set_plaintext_content("This is the text content", mail_body)
        self.mailer.set_reply_to(reply_to, mail_body)
        print('mailer =========',self.mailer,'mai body ------',mail_body)
        # # Removed the set_variables line
        # self.mailer.set_variables(personalization[0]["data"])
        # print("Mail body to be sent:", mail_body)
        # mail_service.send_email(mail_body)
        # print(f"Sending email to {mail_body['recipients'][0]['email']}")
        # print(f"Email content: {mail_body['html_content']}")
        self.mailer.send(mail_body)
        print('mailer send ke bad')

mail_service = MailerSendService()








