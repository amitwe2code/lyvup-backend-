from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserModel
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
# from .custom_auth import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
import os

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def validate_image(self, image):
        """Validate image size and type"""
        if image.size > 5 * 1024 * 1024:
            return {
                'is_valid': False,
                'message': 'Profile picture size should not exceed 5MB'
            }
        
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if image.content_type not in allowed_types:
            return {
                'is_valid': False,
                'message': 'Only JPG and PNG files are allowed'
            }
        
        return {'is_valid': True}

    def get(self, request, pk=None):
        try:
            if pk:
                # Get single user
                user = UserModel.objects.get(pk=pk)
                serializer = UserSerializer(user, context={'request': request})
            else:
                # Get all users
                users = UserModel.objects.all()
                serializer = UserSerializer(users, many=True)

            return Response({
                'status': 'success',
                'message': 'User(s) retrieved successfully',
                'data': serializer.data
            })

        except UserModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('server error')
            return Response({
                'status': 'error',
                'message': 'there is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create new user"""
        try:
            serializer = UserSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                print('request come')
                # Handle profile picture upload
                profile_picture = request.FILES.get('profile_picture')
                if profile_picture:
                    validation_result = self.validate_image(profile_picture)
                    if not validation_result['is_valid']:
                        print('picture validation fail')
                        return Response({
                            'status': 'error',
                            'message': validation_result['message'],
                            'data': None
                        }, status=status.HTTP_400_BAD_REQUEST)

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

    def put(self, request, pk):
        """Update user (Full update)"""
        return self._update_user(request, pk, partial=False)

    def patch(self, request, pk):
        """Update user (Partial update)"""
        return self._update_user(request, pk, partial=True)

    def _update_user(self, request, pk, partial=False):
        """Helper method for user updates"""
        try:
            user = UserModel.objects.get(pk=pk)
            
            # Handle profile picture update
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                # Delete old profile picture
                if user.profile_picture:
                    if os.path.isfile(user.profile_picture.path):
                        os.remove(user.profile_picture.path)
                
                # Validate new profile picture
                validation_result = self.validate_image(profile_picture)
                if not validation_result['is_valid']:
                    return Response({
                        'status': 'error',
                        'message': validation_result['message'],
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserSerializer(user, data=request.data, partial=partial, context={'request': request})
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User updated successfully',
                    'data': serializer.data
                })
            
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except UserModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete user"""
        try:
            user = UserModel.objects.get(pk=pk)
            
            # Delete profile picture if exists
            if user.profile_picture:
                if os.path.isfile(user.profile_picture.path):
                    os.remove(user.profile_picture.path)
            
            user.delete()
            return Response({
                'status': 'success',
                'message': 'User deleted successfully',
                'data': None
            }, status=status.HTTP_204_NO_CONTENT)

        except UserModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
