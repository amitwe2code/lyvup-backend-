from django.urls import path
from .views import ProgramAPIView, AddProgramView

urlpatterns = [
    # path('', ProgramAPIView.as_view(), name='program-list-create'),
    # path('<int:pk>/', ProgramAPIView.as_view(), name='program-detail-update-delete'),
    path('', AddProgramView.as_view(), name='add_program'),
    path('<int:pk>/', AddProgramView.as_view(), name='add_detail_program'),
    path('<int:pk>/', AddProgramView.as_view(), name='add_detail_program'),

]