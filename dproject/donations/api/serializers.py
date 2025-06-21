from rest_framework import serializers
from donations.models import Donation
from accounts.api.serializers import UserBriefSerializer

class DonationSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'user', 'project', 'project_title', 'amount', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Donation amount must be greater than zero.")
        return value