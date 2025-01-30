from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Program
from programactivity.models import ProgramActivityModel
from programactivity.models import ProgramActivityModel
from .serializers import ProgramSerializer, CreateProgramSerializer, GetProgramSerializer
from lyvupapp.pagination import Pagination  # Custom pagination


class AddProgramView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description']
    # search_fields = ['id','name', 'description', 'written_by', 'version', 'price']
    ordering_fields = ['id', 'name', 'description', 'written_by', 'version', 'price','created_at', 'updated_at']
    filterset_fields = ['id', 'name', 'description', 'written_by', 'version', 'price','created_at', 'updated_at']
    pagination_class = Pagination


    def post(self, request):
        try:
            serializer = CreateProgramSerializer(data=request.data)
            print('program post request ')
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
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message':  f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request, pk=None):
        try : 
            if pk:
                try:
                    program = Program.objects.get(pk=pk, is_deleted=0)
                    serializer = GetProgramSerializer(program)
                    return  Response({
                        'status': 'success',
                        'message': 'Program retrieved successfully',
                        'data': serializer.data
                    }, status=status.HTTP_200_OK)
                except Program.DoesNotExist:
                    return Response({
                    'status': 'error',
                    'message': 'program not found',
                    'data': 'None'
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                programs = Program.objects.filter(is_deleted=0)
                programs = DjangoFilterBackend().filter_queryset(request, programs, self)
                programs = SearchFilter().filter_queryset(request, programs, self)
                programs = OrderingFilter().filter_queryset(request, programs, self)
                paginator = self.pagination_class()
                paginated_accounts = paginator.paginate_queryset(programs, request)
                serializer =  GetProgramSerializer(paginated_accounts, many=True)

                return paginator.get_paginated_response(serializer.data)
        except Program.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Program not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            print('pk is=>', pk)
            print('request.data=>', request.data)
            program = Program.objects.get(pk=pk, is_deleted=0)
            serializer = GetProgramSerializer(program, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'consent created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
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

    def delete(self, request, pk):
        try:
            program = Program.objects.get(pk=pk)
            # program.is_deleted = 1
            program.save()
            program.soft_delete()
            return Response({
                'status': 'success',
                'message': 'program deleted successfully',
                'data':'None'
            }, status=status.HTTP_200_OK)
        except Program.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'program not found',
                'data': 'None'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': 'None'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CopyProgram(APIView):
     def post(self,request):
          print('copy program call')
          data=request.data
          id=data.get('isCopyProgram')
          program=Program.objects.get(id=id)
          print('program get =>',program)
          programactivities=ProgramActivityModel.objects.filter(program_id=id)
        #   print('programactivite in copy =====>',programactivities)
          print('get done')
          serializer=ProgramSerializer(data=data)
          if serializer.is_valid():
            copyprogram=serializer.save()
            for activity in programactivities:
                ProgramActivityModel.objects.create(     
                    program_id=copyprogram,  
                    week_no=activity.week_no,
                    activity_id=activity.activity_id,
                    activity_type=activity.activity_type,
                    language=activity.language,
                    activity=activity.activity,
                    brand=activity.brand,
                    who=activity.who,
                    completion_check=activity.completion_check,
                    show_completed=activity.show_completed,
                    location=activity.location,
                    user_duration=activity.user_duration,
                    teamlead_duration=activity.teamlead_duration,
                    coach_duration=activity.coach_duration,
                    coach_type=activity.coach_type,
                    travel_time=activity.travel_time,
                    url=activity.url,
                    amount=activity.amount,
                    file=activity.file,
                    upload_possible=activity.upload_possible,
                    activity_description=activity.activity_description,
                    activity_name=activity.activity_name,
                    send_reminder=activity.send_reminder,
                    show_in_task=activity.show_in_task,
                    add_comment_option=activity.add_comment_option,
                    indicate_when_completed=activity.indicate_when_completed,
                    day=activity.day,
                    time=activity.time,
                )
                
            print('copied program=>',copyprogram)
            return Response({
                    'status':'200 ok ',
                    'message':'Program copied successfully'
                },status=status.HTTP_200_OK)
                         