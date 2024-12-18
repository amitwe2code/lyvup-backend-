from mailersend import emails
from django.conf import settings
# from mailersend import email_verification
from dotenv import load_dotenv
import os
class MailerSendService:
    load_dotenv()


    def get_all_lists(self):
        self.mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))
        response=self.mailer.get_all_lists()
        print('res=>',response)

        
    def send_email(self):
        self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

        # define an empty dict to populate with mail values
        mail_body = {}

        mail_from = {
            "name": "lyvup",
            "email": 'MS_c3k66C@trial-pq3enl6o297l2vwr.mlsender.net',
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
        personalization = [
            {
                "email": "recipient@email.com",
                "data": {
                    "name": "amit",
                    "support_email": "amitpatidar.we2code@gmail.com"
                }
            }
        ]
        self.mailer.set_mail_from(mail_from, mail_body)
        self.mailer.set_mail_to(recipients, mail_body)
        self.mailer.set_subject("Login Success", mail_body)
        self.mailer.set_html_content("<h1>login success</h1><br/><p>login success now you can perform your task</p>", mail_body)
        # self.mailer.set_template("vywj2lp692q47oqz", mail_body)
        self.mailer.set_plaintext_content("This is the text content", mail_body)
        self.mailer.set_reply_to(reply_to, mail_body)
        # self.mailer.set_variables(personalization[0]["data"])
        self.mailer.send(mail_body)


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
