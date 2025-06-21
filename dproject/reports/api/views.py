from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reports.models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Report.objects.filter(project_id=project_id)
        return Report.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)