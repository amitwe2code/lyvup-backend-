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
from .serializers import combinedata
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
                programactivity=ProgramActivityModel.objects.get(id=pk)
                serializer=ProgramActivitySerializer(programactivity,context={'request':request})
                return Response({
                    'status':'success',
                    'message':'week retrieved successfully',
                    'data':serializer.data
                },status=status.HTTP_200_OK)
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
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            data = request.data
            program_id = int(data.get('program_id'))
            week_no =int(data.get('week_no'))
            activity_id=data.get('activity_id')
            if not activity_id : # no activity_id then  request come here to create empty week 
                # all activitys which week_no is greater then incoming week_no set it week_no =week_no+1 for mid week add
                programActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no__gte=week_no) # // __gte greate than equal to  
                if programActivitys.count()>=1 :  # for mid_week set all exist weeek_no=week_no+1
                     for activity in programActivitys :
                          activity.week_no=activity.week_no+1
                          activity.save()
                  
                serializer=ProgramActivitySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status':'200 ok',
                        'message':f'week {week_no} created',
                        'data':'None'
                    },status=status.HTTP_200_OK)
            data=combinedata(data)
            program = Program.objects.get(id=program_id)
            activity=Activity.objects.get(id=activity_id)
            existing_activities = ProgramActivityModel.objects.filter(program_id=program_id, week_no=week_no)
             # if there one data means week is empty there is one data then update that data 
            if existing_activities.count() == 1 and (existing_activities.first().activity_id=='' or existing_activities.first().activity_id is None): 
                existing_activity = existing_activities.first()
                serializer = ProgramActivitySerializer(existing_activity, data=data, partial=True)
                if serializer.is_valid():
                    updated_activity = serializer.save()
                    return Response({
                        'status': 'success',
                        'message': f'Activity assign in week {week_no} ',
                        'data': serializer.data
                    }, status=status.HTTP_200_OK)
                return Response({
                    'status': 'error',
                    'message': 'Validation error',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)      
            else:   # add activity in that weeek which has already atleast one activity and request come with activity_id also that come here     
                serializer = ProgramActivitySerializer(data=data, context={'request': request})
                if serializer.is_valid():
                    new_activity = serializer.save()
                    return Response({
                        'status': 'success',
                        'message': f'Activity assign in week {week_no} ',
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
                'message': 'Program is not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)        
        except Activity.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Activity is not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)        
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
                activity=serializer.save()
                return Response({
                    'status': 'success',
                    'message': f'activity updated in week {activity.week_no}   ',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except ProgramActivityModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Week Activity not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ActivityDelete(APIView):
    def post(self,request):
        try:
            # Retrieve the activity to be delete
            # print('pk =',pk)
            print('request come ')
            data=request.data
            activity_id=data.get('activity_id')
            program_id=data.get('program_id')
            week_no=data.get('week_no')
            program=Program.objects.get(id=program_id)
            if activity_id is None or activity_id =='': # delete week condition
                getWeekActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
                getAllprogramActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no__gte=week_no)
                getWeekActivitys.delete()
                if getAllprogramActivitys.count()>=1:  #geter all week_no set to week_no-1 
                    for activity in getAllprogramActivitys :
                        activity.week_no=activity.week_no-1
                        activity.save()
                elif (int(week_no)==1):  # if delete week is first week 
                    response= ProgramActivityModel.objects.create(week_no=week_no,program_id=program)
                return Response({
                    'status':'success ',
                    'message':f'week {week_no} delete '
                   },status=status.HTTP_200_OK)   
            getWeekActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
            activity = ProgramActivityModel.objects.get(pk=activity_id)
            if getWeekActivitys.count()==1:  # if last activity inside week then create empty week of that week_no previouns two line working on that condition
                activity.delete()
                response= ProgramActivityModel.objects.create(week_no=week_no,program_id=program)
                return Response({
                    'status':'200 ok ',
                    'message':'activity delete in week'
                },status=status.HTTP_200_OK)
            activity.delete()
            return Response({
                    'status':'200 ok ',
                    'message':'activity delete in week',
                    'data':'none'
                },status=status.HTTP_200_OK)
                   
            
        except Program.DoesNotExist:
                        return Response({
                            'status': 'error',
                            'message': 'program not found',
                            'data': None
                        }, status=status.HTTP_404_NOT_FOUND)        
            
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
                        'data': str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           

class CopyWeek(APIView):
     def post(self ,request):
        try:
            data=request.data
            program_id=data.get('program_id')
            week_no=data.get('week_no')
            newWeek=data.get('newWeek')  #last week_no  which assign copy week 
            weekActivities=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
            if weekActivities.count()==1 and (weekActivities.first().activity_id=='' or weekActivities.first().activity_id==None): # week empty condition check then create empty copy week
                  program=Program.objects.get(id=program_id)
                  response= ProgramActivityModel.objects.create(
                    week_no=newWeek,
                    program_id=program)
                  return Response({
                            'status':'200 ok',
                            'message':'week copy successful',
                            },status=status.HTTP_200_OK)   
            for activity in weekActivities:
                data={
                        'program_id':program_id,
                        'activity_id':activity.activity_id,
                        'week_no':newWeek,
                        'day':activity.day,
                        'time':activity.time,
                }
                newProgramActivity=combinedata(data)
               
                serializer=ProgramActivitySerializer(data=newProgramActivity)
                if serializer.is_valid():
                        serializer.save()
                        print('chla 2 ')
            return Response({
                            'status':'success',
                            'message':f'week {week_no} is copied successful',
                            'data':'none'
                            },status=status.HTTP_200_OK)            
        except Exception as e :
            print(f'Server error: {str(e)}')
            return Response({
                        'status': 'error',
                        'message': 'There is some server error',
                        'data': str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   