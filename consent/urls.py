from django.urls import path
from .views import ConsentAPIView

urlpatterns = [
    path('',ConsentAPIView.as_view(),name='ConsentAPIView'),
    path('<int:pk>/',ConsentAPIView.as_view(),name='ConsentAPIView'),
]
