from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from donations.models import Donation
from .serializers import DonationSerializer

class DonationViewSet(viewsets.ModelViewSet):
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Donation.objects.filter(project_id=project_id)
        return Donation.objects.none()

    def perform_create(self, serializer):
        donation = serializer.save(user=self.request.user)
        project = donation.project
        project.current_amount += donation.amount
        project.save()

    @action(detail=False, methods=['get'], url_path='my-donations', permission_classes=[IsAuthenticated])
    def my_donations(self, request):
        donations = Donation.objects.filter(user=request.user).select_related('project')
        serializer = self.get_serializer(donations, many=True)
        return Response(serializer.data)