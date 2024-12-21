from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AccountModelCreate, AccountModelList, AccountModelDetail



urlpatterns = [
    path('create/', AccountModelCreate.as_view(), name='account-create'),
    path('accounts/', AccountModelList.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountModelDetail.as_view(), name='account-detail'),
]
