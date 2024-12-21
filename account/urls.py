from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CreateAccountView, AccountListView, AccountDetailView, AccountUpdateView, AccountDeleteView




urlpatterns=[
    path('', AccountListView.as_view(), name='account-list'),  
    path('create/', CreateAccountView.as_view(), name='create-account'),  
    path('<int:pk>/', AccountDetailView.as_view(), name='account-detail'),  
    path('<int:pk>/update/', AccountUpdateView.as_view(), name='account-update'),  
    path('<int:pk>/delete/', AccountDeleteView.as_view(), name='account-delete'),
]