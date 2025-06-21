# ratings/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet

router = DefaultRouter()
router.register('', RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
]
