from django.shortcuts import render
from rest_framework import viewsets
from  .serializer import AccountSerializer
from .models import AccountModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



class AccountViewSet(viewsets.ModelViewSet):
    queryset=AccountModel.objects.all()
    serializer_class=AccountSerializer
    # authentication_classes =[JWTAuthentication]
    # permission_classes=[IsAuthenticated]