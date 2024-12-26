from django.urls import path,include
from .views import UserAccountView,AccountUserView,UserAccountCreateView,UserAccountDeleteView

urlpatterns = [
    path('user/<int:pk>/',UserAccountView.as_view(),name='useraccount'),
    path('account/<int:pk>/',AccountUserView.as_view(),name='accountuser'),
    path('create/',UserAccountCreateView.as_view(),name='useraccountcreate'),
    path('delete/<int:pk>/',UserAccountDeleteView.as_view(),name='useraccountdelete'),
]