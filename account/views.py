# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import AccountModel
# from .serializer import AccountSerializer
from .serializers import AccountSerializer

from .pagination import AccountModelPagination 
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


class CustomAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class AccountModelCreate(CustomAPIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AccountModelList(CustomAPIView):
    def get(self, request):
        accounts = AccountModel.objects.all()
#search by acc name and acc type
        account_name = request.query_params.get('account_name', None)
        if account_name:
            accounts = accounts.filter(account_name__icontains=account_name)
        account_type = request.query_params.get('account_type', None)
        if account_type:
            accounts = accounts.filter(account_type__icontains=account_type)
# filter by organization_id if 
        organization_id = request.query_params.get('organization_id', None)
        if organization_id is not None:
            accounts = accounts.filter(organization_id=organization_id)  
            
        sort_by = request.query_params.get('sort_by', 'created_at')  
        sort_order = request.query_params.get('sort_order', 'desc')  

        valid_sort_fields = [f.name for f in AccountModel._meta.fields]
        if sort_by in valid_sort_fields:
            if sort_order == 'asc':
                accounts = accounts.order_by(sort_by)  
            else:
                accounts = accounts.order_by(f'-{sort_by}')  
        else:
            return Response({"detail": f"Invalid field '{sort_by}' for sorting."}, status=status.HTTP_400_BAD_REQUEST)

        paginator = AccountModelPagination()
        paginated_accounts = paginator.paginate_queryset(accounts, request)
        serializer =  AccountSerializer(paginated_accounts, many=True)
        
        return paginator.get_paginated_response(serializer.data)
class AccountModelDetail(CustomAPIView):
    def get(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            serializer =  AccountSerializer(account)
            return Response(serializer.data)
        except AccountModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            serializer =  AccountSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AccountModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccountModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
