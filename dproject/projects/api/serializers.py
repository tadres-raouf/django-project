from rest_framework import serializers
from projects.models import Project, ProjectTag
from tags.models import Tag
from categories.models import Category
from media.models import ProjectImage
from accounts.api.serializers import UserBriefSerializer

class ProjectImageSerializer(serializers.ModelSerializer):
    name = serializers.ImageField(read_only=True)
    class Meta:
        model = ProjectImage
        fields = ['id', 'name']

class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        fields = ['id', 'project', 'tag']

class ProjectSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    images = ProjectImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Project
        fields = [
            'id', 'user', 'category', 'category_name', 'title', 'details',
            'tags', 'total_target', 'current_amount',
            'end_time', 'is_cancelled', 'images', 'average_rating'
        ]

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            avg = sum(r.value for r in ratings) / ratings.count()
            return round(avg, 2)
        return 0.0

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        validated_data.pop('user', None)  

        request = self.context.get('request')
        user = request.user if request else None

        project = Project.objects.create(user=user, **validated_data)

        for tag in tags:
            ProjectTag.objects.create(project=project, tag=tag)

        images = request.FILES.getlist('images')
        for img in images:
            ProjectImage.objects.create(project=project, name=img)

        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance