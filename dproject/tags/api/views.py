
from rest_framework import viewsets
from tags.models import Tag
from .serializers import TagSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]