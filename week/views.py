from django.shortcuts import render
from .serializers import WeekSerializer
from .models import WeekModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from lyvupapp.pagination import Pagination
class WeekView(APIView):
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
                week=WeekModel.objects.all(id=pk)
                serializer=WeekSerializer(week,context={'request':request})
                return ResourceWarning({
                    'status':'success',
                    'message':'week retrieved successfully',
                    'data':serializer.data
                },status=status.HTTP_200_Ok)
            weeks = WeekModel.objects.all()
            weeks = DjangoFilterBackend().filter_queryset(request, weeks, self)
            weeks = SearchFilter().filter_queryset(request, weeks, self)
            weeks = OrderingFilter().filter_queryset(request, weeks, self)

            paginator = self.pagination_class()
            paginated_weeks = paginator.paginate_queryset(weeks, request)
            serializer = WeekSerializer(paginated_weeks, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except WeekModel.DoesNotExist:
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
            # data['is_active'] = True
            # data['is_deleted'] = False
            print('request data ',data)
            serializer = WeekSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                week = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'activity created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            print("serializer",serializer)
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
            week = WeekModel.objects.get(pk=pk, is_deleted=0)
            serializer = WeekSerializer(week, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WeekModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            print("pk=>",pk)
            week = WeekModel.objects.get(id=pk)
            # activity.delete()
            
            # activity.is_deleted = 1
            # activity.is_active = 0  
            week.delete()
            return Response({
                'status': 'success',
                'message': 'activity deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)

        except WeekModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'activity not found',
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
