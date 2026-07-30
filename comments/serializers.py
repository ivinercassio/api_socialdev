from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'post_title', 'owner', 'owner_username', 'date_published']
        read_only_fields = ['id', 'owner', 'date_published']