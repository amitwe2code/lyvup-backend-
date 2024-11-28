from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrganizerViewSet



router=DefaultRouter()
router.register('',OrganizerViewSet,basename='organization_route')
urlpatterns=[
    path('',include(router.urls))
]