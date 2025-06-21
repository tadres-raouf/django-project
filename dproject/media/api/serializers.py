# media/api/serializers.py

from rest_framework import serializers
from media.models import ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'project', 'name']
