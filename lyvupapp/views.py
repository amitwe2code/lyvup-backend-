from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from userapp.models import UserModel
from .serializers import LoginSerializer



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
                    'message': 'user done not exit',
                    'errors': None,
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not check_password(password, user.password):
                return Response({
                    'status': 'error',
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'passord is invalid ',
                    'errors': None,
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)

          
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
                        'name': user.name if hasattr(user, 'name') else None,
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