from django.urls import path, include

urlpatterns = [
    path('', include('categories.api.urls')),
]
