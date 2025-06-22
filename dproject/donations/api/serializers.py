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

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None
        project = data.get('project')
        amount = data.get('amount')

        if project and user:
            # Prevent donating to your own project
            if project.user == user:
                raise serializers.ValidationError("You cannot donate to your own project.")

            # Prevent donation beyond the project's target
            remaining_amount = project.total_target - project.current_amount
            if amount > remaining_amount:
                raise serializers.ValidationError(
                    f"Donation exceeds remaining target. You can donate up to {remaining_amount} EGP."
                )

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
