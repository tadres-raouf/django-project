from django.urls import path, include

urlpatterns = [
    path('', include('projects.api.urls')),
]