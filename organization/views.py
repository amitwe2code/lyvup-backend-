from django.shortcuts import render
from rest_framework import viewsets
from .models import OrganizationModel
from .serializer import OrganizationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class OrganizerViewSet(viewsets.ModelViewSet):
    queryset=OrganizationModel.objects.all()
    serializer_class=OrganizationSerializer
    authentication_classes =[JWTAuthentication]
    permission_classes=[IsAuthenticated]