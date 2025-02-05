from django.urls import path, include
from .views import NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view()),
    path('<int:pk>/',NotificationListView.as_view()),
]
