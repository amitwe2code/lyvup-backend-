
from django.contrib import admin
from django.urls import path,include
from .views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import LogoutView,SignupView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('userapp.urls')),
    path('account/',include('account.urls')),
    path('organization/',include('organization.urls')),
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh_view'),
    path('forgot/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('reset/<uidb64>/<token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('useraccount/',include('useraccount.urls')),
    path('survey/',include('survey.urls')),
    path('activityapp/',include('activityapp.urls')),
    path('program/', include('program.urls')),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)