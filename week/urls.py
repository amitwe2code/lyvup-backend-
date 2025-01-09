from django.urls import path
from .views import WeekView


urlpatterns=[
    path('',WeekView.as_view()),
    path('<int:pk>/', WeekView.as_view()),
]