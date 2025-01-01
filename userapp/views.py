from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserModel
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
# from .custom_auth import CustomJWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from lyvupapp.pagination import Pagination
import os

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    search_fields = ['name', 'email', 'phone','id']
    ordering_fields = ['name', 'email','id','phone','user_type','created_at','updated_at']
    filterset_fields = ['user_type','name'] 
    pagination_class = Pagination
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
                return Response({
                    'status': 'success',
                    'message': 'User retrieved successfully',
                    'data': serializer.data
                })
            else:
                # Get all users
                users = UserModel.objects.all()
                users = DjangoFilterBackend().filter_queryset(request, users, self)
                users = SearchFilter().filter_queryset(request, users, self)
                users = OrderingFilter().filter_queryset(request, users, self)
                paginator = self.pagination_class()
                paginated_users = paginator.paginate_queryset(users, request)
                
                serializer = UserSerializer(paginated_users, many=True, context={'request': request})
                return paginator.get_paginated_response(serializer.data)

        except UserModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('server error:', str(e))
            return Response({
                'status': 'error',
                'message': 'there is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create new user"""
        try:
            print('request=>',request)
            print('data=',request.data)
            serializer = UserSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                print('request come')
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
            print('pk=',pk)
            user = UserModel.objects.get(pk=pk)
            print('user=>',user)
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
            print('serialize',serializer)
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
                'message': 'internal error he ',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete user"""
        print('pk=',pk)
        try:
            user = UserModel.objects.get(pk=pk)
             
            user.is_deleted = 1
            # intervention.is_active = 0  
            user.save()
            # Delete profile picture if exists
            if user.profile_picture:
                if os.path.isfile(user.profile_picture.path):
                    os.remove(user.profile_picture.path)
            
            # user.delete()
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
