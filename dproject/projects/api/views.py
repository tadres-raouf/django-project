from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from projects.models import Project, ProjectTag
from .serializers import ProjectSerializer, ProjectTagSerializer
from ratings.models import Rating
from tags.models import Tag


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'tags__name']
    filterset_fields = ['category']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admin can delete projects.")
        instance.delete()

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        project = self.get_object()
        tags = project.tags.values_list('id', flat=True)
        similar_projects = Project.objects.filter(tags__in=tags).exclude(id=project.id).distinct()[:4]
        serializer = self.get_serializer(similar_projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='average-rating')
    def average_rating(self, request, pk=None):
        project = self.get_object()
        ratings = Rating.objects.filter(project=project)
        avg = round(sum(r.value for r in ratings) / ratings.count(), 2) if ratings.exists() else 0.0
        return Response({'rating': avg}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='my-rating', permission_classes=[IsAuthenticated])
    def my_rating(self, request, pk=None):
        project = self.get_object()
        rating = Rating.objects.filter(project=project, user=request.user).first()
        return Response({'rating': rating.value if rating else 0}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='rate', permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        project = self.get_object()
        try:
            value = int(request.data.get('rating'))
            if not (1 <= value <= 5):
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {'error': 'Rating must be an integer between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating, created = Rating.objects.update_or_create(
            project=project,
            user=request.user,
            defaults={'value': value}
        )

        return Response(
            {'rating': value, 'message': 'Rating submitted successfully'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='my-projects', permission_classes=[IsAuthenticated])
    def my_projects(self, request):
        projects = Project.objects.filter(user=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        projects = Project.objects.annotate(
            avg_rating=Avg('ratings__value')
        ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
        latest_projects = Project.objects.order_by('-start_time')[:5]
        serializer = self.get_serializer(latest_projects, many=True)
        return Response(serializer.data)


class ProjectTagViewSet(viewsets.ModelViewSet):
    queryset = ProjectTag.objects.all()
    serializer_class = ProjectTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]