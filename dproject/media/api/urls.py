# media/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectImageViewSet

router = DefaultRouter()
router.register('project-images', ProjectImageViewSet, basename='project-images')

urlpatterns = [
    path('', include(router.urls)),
]
