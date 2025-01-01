from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from userapp.models import UserModel
from mailersend import emails
from django.conf import settings
from .mail_service import mail_service
from .mail_service import MailerSendService
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator  
from django.utils.http import urlsafe_base64_encode  
from .serializers import ForgotPasswordSerializer,ResetPasswordSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from userapp.serializers import UserSerializer


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'code': 'VALIDATION_ERROR',
                    'message': 'data is not valid',
                    'errors': serializer.errors,
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = UserModel.objects.get(email=email)
                print('password in user=>',user.password)
            except UserModel.DoesNotExist:
                return Response({
                    'status': 'error',
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'user does not exist',
                    'errors': None,
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not check_password(password, user.password):
                return Response({
                    'status': 'error',
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'password is invalid ',
                    'errors': None,
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
            # try:
            #     print(f"Attempting to send email to: {user.email}")
            #     mail_service.send_email()

            #     print("Email sent successfully")    
            # except Exception as e:
            #     print(f"Email sending error: {str(e)}")
            #     print(f"Continuing login process despite email error")

            refresh = RefreshToken.for_user(user)
            refresh['user_id'] = user.id  # Explicitly add user ID
            refresh['email'] = user.email
            
            return Response({
                'status': 'success',
                'code': 'LOGIN_SUCCESS',
                'message': 'login successfull',
                'errors': None,
                'data': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'user': { 
                        'id': user.id,
                        'email': user.email,
                        'name': user.name ,
                        'user_type':user.user_type,
                        
                    }
                }
            }, status=status.HTTP_200_OK)
                                
        except Exception as e:
            return Response({
                'status': 'error',
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'something goes to wrong',
                'errors': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SignupView(APIView):
    def post(self, request):
        """Create new user"""
        try:
            print('request=>',request)
            print('data=',request.data)
            serializer = UserSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                print('request come')
                profile_picture = request.FILES.get('profile_picture')
                # if profile_picture:
                #     validation_result = self.validate_image(profile_picture)
                #     if not validation_result['is_valid']:
                #         print('picture validation fail')
                #         return Response({
                #             'status': 'error',
                #             'message': validation_result['message'],
                #             'data': None
                #         }, status=status.HTTP_400_BAD_REQUEST)

                user = serializer.save()
                print('success response')
                return Response({
                    'status': 'success',
                    'message': 'User created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            print('any serailizer error')
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('server error')
            return Response({
                'status': 'error',
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print('email in forget=',email)
            user = get_user_model().objects.get(email=email)
        print('request come ')
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())
        reset_url = f"{settings.FRONTEND_URL}?uid={uid}&token={token}"
        print(f"Generated reset URL: {reset_url}")
        mail_body = {
            "subject": "Password Reset Request",
            "html_content": f"<h1>Password Reset</h1><p>Click the link below to reset your password:</p><p><a href='{reset_url}'>Reset Password</a></p>",
            "plaintext_content": f"Password Reset: Visit the following link to reset your password: {reset_url}",
            "mail_from": {
                "name": "Your App",
                "email": "MS_GTsCGY@trial-pxkjn41epk6lz781.mlsender.net"
            },
            "recipients": [{
                "email": user.email
            }]
        }
        try:
            mail_service = MailerSendService()  
            response = mail_service.send_email(mail_body) 
            if response.status_code == 202:  
                return Response({
                    'status': 'success',
                    'message': 'Password reset email sent successfully',
                    'reset_url': reset_url
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': f"Failed to send email. Status code: {response.status_code}, Response: {response.text}",
                    'data': None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'status': 'error',  
                'message': f"Error sending email: {str(e)}",
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ResetPasswordView(APIView):
   def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (ValueError, TypeError, get_user_model().DoesNotExist):
            return Response({
                'status': 'error',
                'message': 'Invalid or expired token',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({
                'status': 'error',
                'message': 'Invalid or expired token',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['password']
            user.password = make_password(new_password)
            user.save()

            return Response({
                'status': 'success',
                'message': 'Password reset successfully',
                'data': None
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': serializer.errors,
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            access_token = request.data.get("access_token")
            refresh_token = request.data.get("refresh_token")

            if not access_token or not refresh_token:
                return Response({
                    'status': 'error',
                    'message': 'Both access token and refresh token are required for logout',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()  
            except TokenError as e:
                return Response({
                    'status': 'error',
                    'message': f'Invalid refresh token: {str(e)}',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                access = AccessToken(access_token)
               
                self.blacklist_access_token(access_token)  
            except TokenError as e:
                return Response({
                    'status': 'error',
                    'message': f'Invalid access token: {str(e)}',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': 'success',
                'message': 'Logout successful',
                'data': None
            }, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Internal server error',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def blacklist_access_token(self, access_token):
        from datetime import datetime
        