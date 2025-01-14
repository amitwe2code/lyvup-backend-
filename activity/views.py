from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Activity
from .serializers import ActivitySerializer
from lyvupapp.pagination import Pagination


class ActivityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [ 'id', 'activity_type', 'language', 'activity', 'brand', 'who', 
         'completion_check', 'send_reminder']
    ordering_fields = ['id', 'activity_type', 'language', 'activity', 'brand', 'who', 
         'completion_check', 'send_reminder',]
    filterset_fields = ['id', 'activity_type', 'language', 'activity', 'brand', 'who', 
        'completion_check']
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                activity = Activity.objects.get(id=pk)
                serializer = ActivitySerializer(activity, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'activity retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)   
            
            activitys = Activity.objects.all()
            activitys = DjangoFilterBackend().filter_queryset(request, activitys, self)
            activitys = SearchFilter().filter_queryset(request, activitys, self)
            activitys = OrderingFilter().filter_queryset(request, activitys, self)

            paginator = self.pagination_class()
            paginated_activitys = paginator.paginate_queryset(activitys, request)
            serializer = ActivitySerializer(paginated_activitys, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except Activity.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'activity not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            # data['is_active'] = True
            # data['is_deleted'] = False
            print('request data ',data)
            serializer = ActivitySerializer(data=data, context={'request': request})

            if serializer.is_valid():
                activity = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'activity created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            print("serializer",serializer)
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        return self._update_activity(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_activity(request, pk, partial=True)
    def _update_activity(self, request, pk, partial=False):
        try:
            activity = Activity.objects.get(id=pk)
            serializer = ActivitySerializer(activity, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                # Set the updated_by field to the current user
                activity.updated_by = request.user
                activity = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'activity updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Activity.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'activity not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            print("pk=>",pk)
            activity = Activity.objects.get(id=pk)
            # activity.delete()
            
            # activity.is_deleted = 1
            # activity.is_active = 0  
            activity.delete()
            return Response({
                'status': 'success',
                'message': 'activity deleted successfully',
                # 'data': None
            }, status=status.HTTP_204_NO_CONTENT)

        except Activity.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'activity not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
