from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Program
from .serializers import ProgramSerializer
from lyvupapp.pagination import Pagination  # Custom pagination

class ProgramAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['id', 'name', 'written_by', 'version', 'price',  'created_at', 'updated_at']
    ordering_fields = ['id', 'name', 'written_by', 'version', 'price',  'created_at', 'updated_at']
    filterset_fields = ['id', 'name', 'written_by', 'version', 'price', 'created_at', 'updated_at']
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                program = Program.objects.get(id=pk)
                serializer = ProgramSerializer(program, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'Program retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            programs = Program.objects.all()
            programs = DjangoFilterBackend().filter_queryset(request, programs, self)
            programs = SearchFilter().filter_queryset(request, programs, self)
            programs = OrderingFilter().filter_queryset(request, programs, self)

            paginator = self.pagination_class()
            paginated_programs = paginator.paginate_queryset(programs, request)
            serializer = ProgramSerializer(paginated_programs, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except Program.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Program not found',
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
            serializer = ProgramSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                program = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Program created successfully',
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
        return self._update_program(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_program(request, pk, partial=True)

    def _update_program(self, request, pk, partial=False):
        try:
            program = Program.objects.get(id=pk)
            serializer = ProgramSerializer(program, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                program = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Program updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Program.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Program not found',
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
            program = Program.objects.get(id=pk)
            program.is_deleted = 1
            program.save()

            # program.is_active = False  
            # program.save()
            return Response({
                'status': 'success',
                'message': 'Program deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)

        except Program.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Program not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   