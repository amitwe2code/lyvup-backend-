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
            program_id = int(data.get('program_id'))
            week_no =int(data.get('week_no'))
            activity_id=data.get('activity_id')
              
            print('request data =',data)
            if activity_id :
                print('yha nahi jana tha')
                try:
                    activity = Activity.objects.get(id=activity_id)
                except Activity.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': 'Activity not found',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                print('yha aaana he ')    
                serializer=ProgramActivitySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status':'200 ok',
                        'message':'activity create successfully '
                    },status=status.HTTP_200_OK)
            data=combinedata(data)
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
    
    def delete(self,request,pk):
        try:
            # Retrieve the activity to be deleted

            print('request come ')
            data=request.data
            activity_id=data.get('activity_id')
            program_id=data.get('program_id')
            week_no=data.get('week_no')
            print('request data =>',data)
            if activity_id is None or activity_id =='':
                print('all delete ')
                getAllWeekActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
                print('geta ll data ===',getAllWeekActivitys)
                getAllWeekActivitys.delete()
                if(week_no==1):
                   response= ProgramActivityModel.objects.create(week_no=week_no,program_id=program_id)
                return Response({
                       'status':'200 ok ',
                       'message':'week delete successfully'
                   },status=status.HTTP_200_OK)   
            if week_no == 1 :
                print('week on 1 delete ')
                getAllWeekActivitys=ProgramActivityModel.objects.filter(program_id=program_id,week_no=week_no)
                activity = ProgramActivityModel.objects.get(pk=activity_id)
                activity.delete()
                if getAllWeekActivitys.count()==1:
                    response= ProgramActivityModel.objects.create(week_no=week_no,program_id=program_id)
                return Response({
                       'status':'200 ok ',
                       'message':'activity delete successfully'
                   },status=status.HTTP_200_OK)   
            activity = ProgramActivityModel.objects.get(pk=activity_id)
            activity.delete()
            print('any delte ')
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
