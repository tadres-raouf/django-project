from django.urls import path, include

urlpatterns = [
    path('', include('tags.api.urls')),
]
