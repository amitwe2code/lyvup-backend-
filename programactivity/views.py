from django.shortcuts import render
from .serializers import ProgramActivitySerializer
from .models import ProgramActivityModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from activity.models import Activity
from program.models import Program

from lyvupapp.pagination import Pagination
class ProgramActivityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['program_id','week_no']
    ordering_fields = ['program_id','week_no']
    filterset_fields = ['program_id','week_no']
    pagination_class = Pagination
    
    def get(self,request,pk=None):
        try:
            if pk:
                programactivity=ProgramActivityModel.objects.all(id=pk)
                serializer=ProgramActivitySerializer(programactivity,context={'request':request})
                return Response({
                    'status':'success',
                    'message':'week retrieved successfully',
                    'data':serializer.data
                },status=status.HTTP_200_Ok)
            programactivitys = ProgramActivityModel.objects.all()
            programactivitys = DjangoFilterBackend().filter_queryset(request, programactivitys, self)
            programactivitys = SearchFilter().filter_queryset(request, programactivitys, self)
            programactivitys = OrderingFilter().filter_queryset(request, programactivitys, self)

            paginator = self.pagination_class()
            paginated_programactivitys = paginator.paginate_queryset(programactivitys, request)
            serializer = ProgramActivitySerializer(paginated_programactivitys, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except ProgramActivityModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'week not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            data = request.data
            print('request data ',data)
            program_id = data.get('program_id')
            week_no = data.get('week_no')
            id=data.get('activity_id')
            if id:
                try:
                    activity = Activity.objects.get(id=id)
                except Activity.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': 'Activity not found',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
            
            existing_activities = ProgramActivityModel.objects.filter(program_id=program_id, week_no=week_no)
            if program_id:
                try:
                    program = Program.objects.get(id=program_id)
                except Activity.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': 'Progrma is not found',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
            
            existing_activities = ProgramActivityModel.objects.filter(program_id=program_id, week_no=week_no)
            
            if existing_activities.count() == 1:
               
                existing_activity = existing_activities.first()
                print('activity is ------=>',existing_activity)
                print('true/false=>',existing_activity.activity_id == '')
                if existing_activity.activity_id is None or existing_activity.activity_id == '':
                    # Update the existing activity
                    serializer = ProgramActivitySerializer(existing_activity, data=data, partial=True)

                    if serializer.is_valid():
                        # Update fields from the Activity instance
                        existing_activity.update_from_activity(activity)
                        updated_activity = serializer.save()  # Save the updated instance
                        return Response({
                            'status': 'success',
                            'message': 'Program Activity updated successfully',
                            'data': updated_activity
                        }, status=status.HTTP_200_OK)

                    return Response({
                        'status': 'error',
                        'message': 'Validation error',
                        'data': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # If activity_id is not empty, create a new ProgramActivityModel
                    new_data = data.copy()  # Create a copy of the request data
                    new_data['activity_id'] = activity.id
                    print('program get =======>',program) # Set the activity_id from the retrieved activity
                    new_data['program_id']=program  # Set the activity_id from the retrieved activity
                    # Create a new ProgramActivityModel instance
                    new_activity = ProgramActivityModel(**new_data)
                    new_activity.update_from_activity(activity)  # Update fields from the Activity instance
                    serializer = ProgramActivitySerializer(new_activity)
                    print('yha tk aaya ')
                    if serializer.is_valid():
                        print('yha nahi aaya ')
                        print('new data=>',new_data)
                        new_activity = serializer.save()
                        return Response({
                            'status': 'success',
                            'message': 'New Program Activity created successfully',
                            'data': new_activity
                        }, status=status.HTTP_201_CREATED)

                    return Response({
                        'status': 'error',
                        'message': 'Validation error',
                        'data': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ProgramActivitySerializer(data=data, context={'request': request})

                new_data = data.copy()  # Create a copy of the request data
                new_data['activity_id'] = activity.id 
                print('program get =======>',program) # Set the activity_id from the retrieved activity
                new_data['program_id']=program
                # Create a new ProgramActivityModel instance
                new_activity = ProgramActivityModel(**new_data)
                new_activity.update_from_activity(activity)  # Update fields from the Activity instance

                serializer = ProgramActivitySerializer(new_activity)

                if serializer.is_valid():
                    new_activity = serializer.save()
                    return Response({
                        'status': 'success',
                        'message': 'New Program Activity created successfully',
                        'data': new_activity
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
        try:
            print('pk is=>', pk)
            print('request.data=>', request.data)
            week = ProgramActivityModel.objects.get(pk=pk, is_deleted=0)
            serializer = ProgramActivitySerializer(week, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProgramActivityModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            # Retrieve the activity to be deleted
            activity = ProgramActivityModel.objects.get(pk=pk)

            # Check if this is the last activity for the given program_id and week_no
            related_activities = ProgramActivityModel.objects.filter(
                program_id=activity.program_id,
                week_no=1
            )
            if related_activities.count() == 1:
                # If this is the last activity, clear all fields except program_id and week_no
                activity.activity_id = None
                activity.activity_type = None
                activity.language = None
                activity.activity = None
                activity.brand = None
                activity.who = None
                activity.completion_check = None
                activity.show_completed = False  # Default value
                activity.location = None
                activity.user_duration = 0  # Default value
                activity.teamlead_duration = 0  # Default value
                activity.coach_duration = 0  # Default value
                activity.coach_type = None
                activity.travel_time = None
                activity.url = None
                activity.amount = None
                activity.file = None
                activity.upload_possible = 'no'  # Default value
                activity.activity_description = None
                activity.activity_name = None
                activity.send_reminder = 'no'  # Default value
                activity.show_in_task = 'no'  # Default value
                activity.add_comment_option = 'no'  # Default value
                activity.indicate_when_completed = 'no'  # Default value

                # Save the cleared activity
                activity.save()
                return Response({
                    'status': 'success',
                    'message': 'Activity fields cleared successfully',
                }, status=status.HTTP_200_OK)
            else:
                activity.delete()
                return Response({
                    'status': 'success',
                    'message': 'Activity deleted successfully',
                }, status=status.HTTP_204_NO_CONTENT)

        except ProgramActivityModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Activity not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           


# Create your views here.
