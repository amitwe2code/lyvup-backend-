
from django.contrib import admin
from django.urls import path,include
from .views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('userapp.urls')),
    path('account/',include('account.urls')),
    path('organization/',include('organization.urls')),
    path('login/',LoginView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh_view'),
    path('auth/',include('rest_framework.urls',namespace='rest_framework'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)