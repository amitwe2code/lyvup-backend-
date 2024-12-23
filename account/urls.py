from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AccountAPIView


urlpatterns = [
    path('', AccountAPIView.as_view(), name='account-create'),
    path('<int:pk>/', AccountAPIView.as_view(), name='account-list'),
]
