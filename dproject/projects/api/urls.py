# projects/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectTagViewSet

router = DefaultRouter()
router.register('', ProjectViewSet, basename='projects')
router.register(r'tags', ProjectTagViewSet, basename='project-tags')

urlpatterns = [
    path('', include(router.urls)),
]