# ratings/api/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from ratings.models import Rating
from .serializers import RatingSerializer
from rest_framework.decorators import action
from django.db.models import Avg

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Rating.objects.all()

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        existing_rating = Rating.objects.filter(user=self.request.user, project=project).first()
        if existing_rating:
            existing_rating.value = serializer.validated_data['value']
            existing_rating.save()
        else:
            serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_rating(self, request, pk=None):
        try:
            rating = Rating.objects.get(user=request.user, project=pk)
            return Response({'rating': rating.value})
        except Rating.DoesNotExist:
            return Response({'rating': 0})

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        average = Rating.objects.filter(project=pk).aggregate(avg=Avg('value'))['avg']
        return Response({'rating': round(average, 1) if average else 0})
