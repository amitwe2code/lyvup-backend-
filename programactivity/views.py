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
            print(f'Server error: {str(e)}')
            return Response({
                'status': 'error',
                'message': 'There is some server error',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            data = request.data
            program_id = int(data.get('program_id'))
            week_no =int(data.get('week_no'))
            activity_id=data.get('activity_id')
              
            print('request data =',data)
            if activity_id :
                print('activity get ')
                try:
                    activity = Activity.objects.get(id=activity_id)
                except Activity.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': 'Activity not found',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                print('week add  ')
                programActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no__gte=week_no)
                if programActivitys.count()>=1 :
                     print('mid week me aaya he ')
                     for activity in programActivitys :
                          print(' update week in mid week add')
                          activity.week_no=activity.week_no+1
                          activity.save()
                  # // __gte greate than equal to  
                serializer=ProgramActivitySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status':'200 ok',
                        'message':'activity create successfully '
                    },status=status.HTTP_200_OK)
            data=combinedata(data)
            print('combine data =>',data)
            print('step 2')
            if program_id:
                try:
                    program = Program.objects.get(id=program_id)
                except Activity.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': 'Progrma is not found',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
            print('step 3')
            existing_activities = ProgramActivityModel.objects.filter(program_id=program_id, week_no=week_no)
            print('step 4')
            if existing_activities.count() == 1:
                print('step 5')
                existing_activity = existing_activities.first()
                if existing_activity.activity_id is None or existing_activity.activity_id == '':
                    # Update the existing activity
                    print('step 6')
                    serializer = ProgramActivitySerializer(existing_activity, data=data, partial=True)
                    print('step 7')
                    # print('serilizer --=====',serializer)
                    if serializer.is_valid():
                        print('step 8')
                        # Update fields from the Activity instance
                        # existing_activity.update_from_activity(activity)
                        updated_activity = serializer.save()
                        print('step 9')  # Save the updated instance
                        return Response({
                            'status': 'success',
                            'message': 'Program Activity updated successfully',
                            'data': serializer.data
                        }, status=status.HTTP_200_OK)

                    return Response({
                        'status': 'error',
                        'message': 'Validation error',
                        'data': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                  
                    serializer= ProgramActivitySerializer(data=data)
                    print('yha tk aaya ')
                    if serializer.is_valid():
                        print('new data=>',serializer)
                        new_activity = serializer.save()
                        return Response({
                            'status': 'success',
                            'message': 'New Program Activity created successfully',
                            'data': serializer.data
                        }, status=status.HTTP_201_CREATED)

                    return Response({
                        'status': 'error',
                        'message': 'Validation error',
                        'data': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ProgramActivitySerializer(data=data, context={'request': request})

                if serializer.is_valid():
                    new_activity = serializer.save()
                    return Response({
                        'status': 'success',
                        'message': 'New Program Activity created successfully',
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
            print('request data =>',data)
            if activity_id is None or activity_id =='':
                print('all delete ')
                getWeekActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
                print('get all data ===',getWeekActivitys)
                getAllprogramActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no__gte=week_no)
                getWeekActivitys.delete()
                if getAllprogramActivitys.count()>1:
                    print('update next week activitys',getAllprogramActivitys.count())
                    for activity in getAllprogramActivitys :
                        activity.week_no=activity.week_no-1
                        activity.save()
                elif (int(week_no)==1):
                    print('create first empty week ')
                    response= ProgramActivityModel.objects.create(week_no=week_no,program_id=program)
                return Response({
                    'status':'200 ok ',
                    'message':'activity week delete successfully'
                   },status=status.HTTP_200_OK)   
            getWeekActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
            print('total activity in that week =>',getWeekActivitys.count())
            print('total activity in that week =>',getWeekActivitys.count()==1)
            activity = ProgramActivityModel.objects.get(pk=activity_id)
            print('delete activity in out side all ')
            if getWeekActivitys.count()==1:
                print('create empty if it will last activity in week')
                activity.delete()
                response= ProgramActivityModel.objects.create(week_no=week_no,program_id=program)
                return Response({
                    'status':'200 ok ',
                    'message':'activity delete successfully'
                },status=status.HTTP_200_OK)
            activity.delete()
            return Response({
                    'status':'200 ok ',
                    'message':'activity delete successfully'
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
            newWeek=data.get('newWeek')
            print('data=>',data)
            weekActivities=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
            print('weekactivities get',weekActivities)
            if weekActivities.count()<=1:
                  program=Program.objects.get(id=program_id)
                  response= ProgramActivityModel.objects.create(
                    week_no=newWeek,
                    program_id=program)
                  return Response({
                            'message':'week copy successful',
                            'status':'200 ok'
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
            return Response({
                            'message':'week copy successful',
                            'status':'200 ok'
                            },status=status.HTTP_200_OK)            
        except Exception as e :
            print(f'Server error: {str(e)}')
            return Response({
                        'status': 'error',
                        'message': 'There is some server error',
                        'data': str(e)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   