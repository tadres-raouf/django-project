from django.urls import path, include

urlpatterns = [
    path('', include('comments.api.urls')),
]

