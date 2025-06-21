# media/api/views.py

from rest_framework import viewsets
from media.models import ProjectImage  

from .serializers import ProjectImageSerializer

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
