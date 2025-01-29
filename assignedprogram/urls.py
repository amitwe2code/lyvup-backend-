from django.urls import path
from .views import AssigendProgramView

urlpatterns = [
    path('',AssigendProgramView.as_view(),name='AssigendProgramView'),
    path('<int:pk>/',AssigendProgramView.as_view(),name='AssigendProgramView'),
]
