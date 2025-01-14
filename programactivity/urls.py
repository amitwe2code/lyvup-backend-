from django.urls import path
from .views import ProgramActivityView


urlpatterns=[
    path('',ProgramActivityView.as_view()),
    path('<int:pk>/', ProgramActivityView.as_view()),
]