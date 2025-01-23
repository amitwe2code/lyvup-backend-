from django.urls import path
from .views import ProgramActivityView,ActivityDelete,CopyWeek


urlpatterns=[
    path('',ProgramActivityView.as_view()),
    path('<int:pk>/', ProgramActivityView.as_view()),
    path('activitydelete/',ActivityDelete.as_view()),
    path('copy/',CopyWeek.as_view()),
]
