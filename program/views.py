from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Program
from programactivity.models import ProgramActivityModel
from .serializers import ProgramSerializer, CreateProgramSerializer, GetProgramSerializer
from lyvupapp.pagination import Pagination  # Custom pagination


class AddProgramView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['id','name', 'description', 'written_by', 'version', 'price']
    ordering_fields = ['id', 'name', 'description', 'written_by', 'version', 'price','created_at', 'updated_at']
    filterset_fields = ['id', 'name', 'description', 'written_by', 'version', 'price','created_at', 'updated_at']
    pagination_class = Pagination


    def post(self, request):
        try:
            serializer = CreateProgramSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serial_data = serializer.validated_data
                program = Program.objects.create(
                    name=serial_data.get("name"),
                    description=serial_data.get("description"),
                    written_by=serial_data.get("written_by"),
                    version=serial_data.get("version"),
                    price=serial_data.get("price")
                )
                if(program):
                    response= ProgramActivityModel.objects.create(
                    week_no=1,
                    program_id=program)
                    print('response in programactivity create in program',response)
                   
            
                return Response({
                    'status': 'success',
                    'message': 'Program created successfully',
                    'data': {'id': program.id,
                             'name': serial_data.get("name"),
                             'description': serial_data.get("description"),
                             'written_by': serial_data.get("written_by"),
                             'version': serial_data.get("version"),
                             'price': serial_data.get("price")}
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk=None):
        if pk:
            try:
                program = Program.objects.get(pk=pk, is_deleted=0)
                serializer = GetProgramSerializer(program)
                return Response(serializer.data)
            except Program.DoesNotExist:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            programs = Program.objects.filter(is_deleted=0)
            programs = DjangoFilterBackend().filter_queryset(request, programs, self)
            programs = SearchFilter().filter_queryset(request, programs, self)
            programs = OrderingFilter().filter_queryset(request, programs, self)
            paginator = self.pagination_class()
            paginated_accounts = paginator.paginate_queryset(programs, request)
            serializer =  GetProgramSerializer(paginated_accounts, many=True)

            return paginator.get_paginated_response(serializer.data)

    def put(self, request, pk):
        try:
            print('pk is=>', pk)
            print('request.data=>', request.data)
            program = Program.objects.get(pk=pk, is_deleted=0)
            serializer = GetProgramSerializer(program, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Program.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            program = Program.objects.get(pk=pk)
            program.is_deleted = 1
            program.save()

            program.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Program.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

