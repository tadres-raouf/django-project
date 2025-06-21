from rest_framework import serializers
from comments.models import Comment
from accounts.models import User  

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)  

    class Meta:
        model = Comment
        fields = ['id', 'user', 'project', 'content', 'create_at', 'update_at']
        read_only_fields = ['user', 'create_at', 'update_at']