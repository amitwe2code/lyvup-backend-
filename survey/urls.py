from django.urls import path
from .views import InterventionAPIView

urlpatterns = [
    path('', InterventionAPIView.as_view(), name='create-intervention'),
    path('<int:pk>/',InterventionAPIView.as_view(), name='intervention-detail'), 

]
