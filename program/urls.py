from django.urls import path
from .views import ProgramAPIView


urlpatterns = [
    path('', ProgramAPIView.as_view(), name='program-list-create'),
    path('<int:pk>/', ProgramAPIView.as_view(), name='program-detail-update-delete'),

]