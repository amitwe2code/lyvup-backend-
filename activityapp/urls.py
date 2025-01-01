from django.urls import path
from .views import ActivityActionTypeAPIView

urlpatterns = [
    path('', ActivityActionTypeAPIView.as_view(), name='activity-action-type-list'),
    path('<int:pk>/', ActivityActionTypeAPIView.as_view(), name='activity-action-type-detail'),
]
