# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import AccountModel
from .serializers import AccountSerializer
from lyvupapp.pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter


class AccountAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    search_fields = ['account_name','account_type']
    ordering_fields = ['account_name','account_type','language','created_at','updated_at']
    filterset_fields = ['account_name','account_type','organization_id','team_leader_id','id'] 
    pagination_class = Pagination

    def get(self, request,pk=None):
        try:
            if pk:
                try:
                    account = AccountModel.objects.get(pk=pk)
                    serializer =  AccountSerializer(account)
                    return Response({
                        'status': 'success',
                        'message': 'User retrieved successfully',
                        'data': serializer.data
                    },status=status.HTTP_200_OK)
                except AccountModel.DoesNotExist:
                    return Response({
                        'status': 'error',
                        'message': 'Account not found, please check the provided ID',
                        'data': None
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                accounts = AccountModel.objects.all()
                accounts = DjangoFilterBackend().filter_queryset(request, accounts, self)
                accounts = SearchFilter().filter_queryset(request, accounts, self)
                accounts = OrderingFilter().filter_queryset(request, accounts, self)
                paginator = self.pagination_class()
                paginated_accounts = paginator.paginate_queryset(accounts, request)
                serializer =  AccountSerializer(paginated_accounts, many=True)
                return paginator.get_paginated_response(serializer.data)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Accounts not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('server error:', str(e))
            return Response({
                'status': 'error',
                'message':  f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User created successfully',
                    'data': serializer.data
                    }, status=status.HTTP_201_CREATED)
            return Response({
                    'status': 'error',
                    'message': 'Validation error',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({
                'status': 'error',
                'message':  f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    def put(self, request, pk):
        try:
            print('pk is=>',pk)
            print('request.data=>',request.data)
            account = AccountModel.objects.get(pk=pk)
            serializer =  AccountSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Account updated successfully',
                    'data': serializer.data
                },status=status.HTTP_201_CREATED)
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Account not found',
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
            account = AccountModel.objects.get(pk=pk)
            # account.is_deleted = 1
            # account.save()
            account.delete()
            print('ye chla ')
            return Response({
                'status': 'success',
                'message': 'account deleted successfully',
                'data': 'none'
            }, status=status.HTTP_200_OK)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Account not found',
                'data': 'None'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': 'None'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)