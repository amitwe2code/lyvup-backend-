from django.urls import path
from .views import ActivityView

urlpatterns = [
    path('', ActivityView.as_view(), name='create-activity'),
    path('<int:pk>/',ActivityView.as_view(), name='activity-detail'),
]
