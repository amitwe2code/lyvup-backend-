from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import AssignedProgramModel
from .serializers import AssignedProgramSerializer
from lyvupapp.pagination import Pagination
from rest_framework.views import APIView
# Create your views here.
class AssigendProgramView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['id','program_id','assign_to' ]
    ordering_fields = ['id','program_id','assign_to','assign_type' ]
    filterset_fields = ['id','program_id','assign_to','assign_type' ]
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                assignedProgram = AssignedProgramModel.objects.get(id=pk)
                serializer = AssignedProgramSerializer(assignedProgram, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'assignedProgram retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            assignedPrograms = AssignedProgramModel.objects.all().order_by('id')
            
            assignedPrograms = DjangoFilterBackend().filter_queryset(request, assignedPrograms, self)
            assignedPrograms = SearchFilter().filter_queryset(request, assignedPrograms, self)
            assignedPrograms = OrderingFilter().filter_queryset(request, assignedPrograms, self)
            paginator = self.pagination_class()
            paginated_assignedPrograms = paginator.paginate_queryset(assignedPrograms, request)
            serializer = AssignedProgramSerializer(paginated_assignedPrograms, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except AssignedProgramModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'assignedProgram Request not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            print('data=',data)
            serializer = AssignedProgramSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                assignedProgram = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Assigned Program created ',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        return self._update_assignedProgram(request, pk, partial=True)

    def patch(self, request, pk):
        return self._update_assignedProgram(request, pk, partial=True)

    def _update_assignedProgram(self, request, pk, partial=True):
        try:
            assignedProgram = AssignedProgramModel.objects.get(id=pk)
            serializer = AssignedProgramSerializer(assignedProgram, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                assignedProgram = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Assigned Program updated ',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except AssignedProgramModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'assignedProgram Request not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            assignedProgram = AssignedProgramModel.objects.get(id=pk)
            # assignedProgram.is_deleted = True
            assignedProgram.is_deleted = 1 

            assignedProgram.delete()
            return Response({
                'status': 'success',
                'message': 'Assigned Program deleted ',
                'data':'None'
            }, status=status.HTTP_200_OK)

        except AssignedProgramModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'assignedProgram Request not found',
                'data': 'None'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': 'None'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
