# reports/api/serializers.py

from rest_framework import serializers
from reports.models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'project', 'comment', 'reason', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        if not data.get('project') and not data.get('comment'):
            raise serializers.ValidationError("You must report either a project or a comment.")
        if data.get('project') and data.get('comment'):
            raise serializers.ValidationError("You can only report a project or a comment, not both.")
        return data