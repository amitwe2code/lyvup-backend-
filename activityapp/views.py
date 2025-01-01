from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ActivityActionType
from .serializers import ActivityActionTypeSerializer
from lyvupapp.pagination import Pagination


class ActivityActionTypeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['id', 'activity_type', 'activity', 'amount', 'unit', 'key_activity', 'is_active', 'is_deleted', 'created_at', 'updated_at']
    ordering_fields = ['id', 'activity_type', 'activity', 'amount', 'unit', 'key_activity', 'is_active', 'is_deleted', 'created_at', 'updated_at']
    filterset_fields = ['id', 'activity_type', 'activity', 'amount', 'unit', 'key_activity', 'is_active', 'is_deleted', 'created_at', 'updated_at']
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                activity_action_type = ActivityActionType.objects.get(id=pk)
                serializer = ActivityActionTypeSerializer(activity_action_type, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'Activity Action Type retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            activity_action_types = ActivityActionType.objects.all()
            activity_action_types = DjangoFilterBackend().filter_queryset(request, activity_action_types, self)
            activity_action_types = SearchFilter().filter_queryset(request, activity_action_types, self)
            activity_action_types = OrderingFilter().filter_queryset(request, activity_action_types, self)

            paginator = self.pagination_class()
            paginated_activity_action_types = paginator.paginate_queryset(activity_action_types, request)
            serializer = ActivityActionTypeSerializer(paginated_activity_action_types, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except ActivityActionType.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Activity Action Type not found',
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
            serializer = ActivityActionTypeSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                activity_action_type = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Activity Action Type created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

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
        return self._update_activity_action_type(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_activity_action_type(request, pk, partial=True)

    def _update_activity_action_type(self, request, pk, partial=False):
        try:
            activity_action_type = ActivityActionType.objects.get(id=pk)
            serializer = ActivityActionTypeSerializer(activity_action_type, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                activity_action_type = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Activity Action Type updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except ActivityActionType.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Activity Action Type not found',
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
            activity_action_type = ActivityActionType.objects.get(id=pk)
            # activity_action_type.is_deleted = True
            activity_action_type.is_deleted = 1 

            activity_action_type.save()
            return Response({
                'status': 'success',
                'message': 'Activity Action Type deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)

        except ActivityActionType.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Activity Action Type not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
