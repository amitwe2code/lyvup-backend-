# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import AccountSerializer



class CreateAccountView(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountListView(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = AccountModel.objects.all()  
        serializer = self.serializer_class(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountDetailView(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            serializer = self.serializer_class(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Account not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)


class AccountUpdateView(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            serializer = self.serializer_class(account, data=request.data)
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Account not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            serializer = self.serializer_class(account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Account not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)


class AccountDeleteView(APIView):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            account = AccountModel.objects.get(pk=pk)
            account.delete()  
            return Response({
                'status': 'success',
                'message': 'Account deleted successfully',
                'data': None
            }, status=status.HTTP_204_NO_CONTENT)
        except AccountModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Account not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)