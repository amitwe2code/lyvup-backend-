from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Intervention
from .serializers import InterventionSerializer
from lyvupapp.pagination import Pagination


class InterventionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [ 'id', 'intervention_type', 'language', 'activity', 'brand', 'who', 
        'activity_type', 'completion_check', 'send_reminder', 'add_comment_option', 
        'show_completed', 'location', 'user_duration', 'duration_coach', 
        'coach_type', 'url', 'amount', 'file', 'upload_possible', 
        'intervention_description', 'intervention_name', 'show_in_tasks', 
        'is_active', 'is_deleted', 'created_at', 'updated_at']
    ordering_fields = ['id', 'intervention_type', 'language', 'activity', 'brand', 'who', 
        'activity_type', 'completion_check', 'send_reminder', 'add_comment_option', 
        'show_completed', 'location', 'user_duration', 'duration_coach', 
        'coach_type', 'url', 'amount', 'file', 'upload_possible', 
        'intervention_description', 'intervention_name', 'show_in_tasks', 
        'is_active', 'is_deleted', 'created_at', 'updated_at']
    filterset_fields = ['id', 'intervention_type', 'language', 'activity', 'brand', 'who', 
        'activity_type', 'completion_check', 'send_reminder', 'add_comment_option', 
        'show_completed', 'location', 'user_duration', 'duration_coach', 
        'coach_type',  'amount', 
        'intervention_description', 'intervention_name', 'show_in_tasks', 
        'is_active', 'is_deleted', 'created_at', 'updated_at']
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                intervention = Intervention.objects.get(id=pk)
                serializer = InterventionSerializer(intervention, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'Intervention retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)   
            
            interventions = Intervention.objects.all()
            interventions = DjangoFilterBackend().filter_queryset(request, interventions, self)
            interventions = SearchFilter().filter_queryset(request, interventions, self)
            interventions = OrderingFilter().filter_queryset(request, interventions, self)

            paginator = self.pagination_class()
            paginated_interventions = paginator.paginate_queryset(interventions, request)
            serializer = InterventionSerializer(paginated_interventions, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except Intervention.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Intervention not found',
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
            serializer = InterventionSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                intervention = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Intervention created successfully',
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
        return self._update_intervention(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_intervention(request, pk, partial=True)
    def _update_intervention(self, request, pk, partial=False):
        try:
            intervention = Intervention.objects.get(id=pk)
            serializer = InterventionSerializer(intervention, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                # Set the updated_by field to the current user
                intervention.updated_by = request.user
                intervention = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Intervention updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Intervention.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Intervention not found',
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
            intervention = Intervention.objects.get(id=pk)
            # intervention.delete()
            
            intervention.is_deleted = 1
            # intervention.is_active = 0  
            intervention.save()
            return Response({
                'status': 'success',
                'message': 'Intervention deleted successfully',
                # 'data': None
            }, status=status.HTTP_204_NO_CONTENT)

        except Intervention.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Intervention not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
