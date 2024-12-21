from mailersend import emails
from django.conf import settings
from mailersend import email_verification
from dotenv import load_dotenv
import os
import requests

# from mailersend import emails
# from django.conf import settings
# from dotenv import load_dotenv
# import os

class MailerSendService:
    load_dotenv()
    MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')

    def send_email(self, mail_body):
        print(f"MailerSend API Key: {os.getenv('MAILERSEND_API_KEY')}")
        MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')

    def send_email(self, mail_body):
        url = "https://api.mailersend.com/v1/email"
        headers = {
            "Authorization": f"Bearer {self.MAILERSEND_API_KEY}",
            "Content-Type": "application/json"
        }

        # Ensure mail body is structured properly
        mail_body_fixed = {
            "subject": mail_body["subject"],
            "html": mail_body["html_content"],  # HTML content for the email body
            "text": mail_body["plaintext_content"],  # Text content for email
            "from": {
                "email": mail_body["mail_from"]["email"],  # From email address
                "name": mail_body["mail_from"]["name"]
            },
            "to": [{"email": recipient["email"]} for recipient in mail_body["recipients"]]  # Recipients
        }

        # Debugging step: Print the fixed mail body to ensure it is structured correctly
        print(f"Mail Body Sent: {mail_body_fixed}")  # Check this output

        # Send the email using requests.post()
        response = requests.post(url, json=mail_body_fixed, headers=headers)

        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

        return response

        # print(f"MailerSend API Key: {os.getenv('MAILERSEND_API_KEY')}")

        self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
        
        mail_from = {
            "name": "lyvup",
            "email": 'MS_GTsCGY@trial-pxkjn41epk6lz781.mlsender.net',
        }

        recipients = [
            {
                "name": "Your Client",
                "email": 'amitpatidar251@gmail.com',
            }
        ]

        reply_to = {
            "name": "Name",
            "email": "amitpatidar.we2code@gmail.com",
        }

        # self.mailer.set_mail_from(mail_from, mail_body)
        # self.mailer.set_mail_to(recipients, mail_body)
        # self.mailer.set_subject("Login Success", mail_body)
        # self.mailer.set_html_content("<h1>login success</h1><br/><p>login success now you can perform your task</p>", mail_body)
        # self.mailer.set_template("vywj2lp692q47oqz", mail_body)
        # self.mailer.set_plaintext_content("This is the text content", mail_body)
        # self.mailer.set_reply_to(reply_to, mail_body)

        # Removed the set_variables line
        # self.mailer.set_variables(personalization[0]["data"])
        # print("Mail body to be sent:", mail_body)
        # mail_service.send_email(mail_body)
        print(f"Sending email to {mail_body['recipients'][0]['email']}")
        print(f"Email content: {mail_body['html_content']}")
        self.mailer.send(mail_body)
        # print(mail_body["html_content"])


#     load_dotenv()


#     def get_all_lists(self):
#         self.mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))
#         response=self.mailer.get_all_lists()
#         print('res=>',response)
#     def send_email(self):
#         self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

#         # define an empty dict to populate with mail values
#         mail_body = {}

#         mail_from = {
#             "name": "lyvup",
#             "email": 'MS_c3k66C@trial-pq3enl6o297l2vwr.mlsender.net',
#         }

#         recipients = [
#             {
#                 "name": "Your Client",
#                 "email": 'amitpatidar251@gmail.com',
#             }
#         ]

#         reply_to = {
#             "name": "Name",
#             "email": "amitpatidar.we2code@gmail.com",
#         }
#         personalization = [
#             {
#                 "email": "recipient@email.com",
#                 "data": {
#                     "name": "amit",
#                     "support_email": "amit@gmail.com"
#                 }
#             }
#         ]
#         self.mailer.set_mail_from(mail_from, mail_body)
#         self.mailer.set_mail_to(recipients, mail_body)
#         self.mailer.set_subject("Login Success", mail_body)
#         self.mailer.set_html_content("<h1>login success</h1><br/><p>login success now you can perform your task</p>", mail_body)
#         self.mailer.set_template("vywj2lp692q47oqz", mail_body)
#         self.mailer.set_plaintext_content("This is the text content", mail_body)
#         self.mailer.set_reply_to(reply_to, mail_body)
#         self.mailer.set_variables(personalization[0]["data"])
#         self.mailer.send(mail_body)
mail_service = MailerSendService()




# views.py

# from django.core.mail import send_mail
# from django.conf import settings

# def send_test_email(request):
#     subject = "Test Email from Django"
#     message = "This is a test email sent from Django using Mailersend SMTP."
#     from_email = settings.EMAIL_HOST_USER  # From email configured in settings.py
#     recipient_list = ["amitpatidar251@gmail.com"]  # Replace with recipient's email
    
#     try:
#         # Send the email
#         send_mail(subject, message, from_email, recipient_list)
#         return HttpResponse("Email sent successfully!", content_type="text/plain")
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", content_type="text/plain")











# //created by amit for in first email send 
# from mailersend import emails
# from django.conf import settings
# # from mailersend import email_verification
# from dotenv import load_dotenv
# import os
# class MailerSendService:
#     load_dotenv()
        
#     def send_email(self):
#         self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
#         mail_body = {}

#         mail_from = {
#             "name": "lyvup",
#             "email": 'MS_c3k66C@trial-pq3enl6o297l2vwr.mlsender.net',
#         }

#         recipients = [
#             {
#                 "name": "Your Client",
#                 "email": 'amitpatidar251@gmail.com',
#             }
#         ]

#         reply_to = {
#             "name": "Name",
#             "email": "amitpatidar.we2code@gmail.com",
#         }
       
    
#         self.mailer.set_mail_from(mail_from, mail_body)
#         self.mailer.set_mail_to(recipients, mail_body)
#         self.mailer.set_subject("Login Success", mail_body)
#         self.mailer.set_html_content("<h1>login success</h1><br/><p>login success now you can perform your task</p>", mail_body)
#         self.mailer.set_plaintext_content("This is the text content", mail_body)
#         self.mailer.set_reply_to(reply_to, mail_body)
#         self.mailer.send(mail_body)


# mail_service = MailerSendService()
