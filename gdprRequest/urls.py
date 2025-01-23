from django.urls import path
from .views import GDPRAPIView

urlpatterns = [
    path('',GDPRAPIView.as_view(),name='GDPRAPIView'),
    path('<int:pk>/',GDPRAPIView.as_view(),name='GDPRAPIView'),
]
