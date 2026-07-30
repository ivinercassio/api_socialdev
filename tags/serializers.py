from rest_framework import serializers
from .models import Tag, PostTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'theme']


class PostTagSerializer(serializers.ModelSerializer):
    tag_theme = serializers.ReadOnlyField(source='tag.theme')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = PostTag
        fields = ['id', 'tag', 'tag_theme', 'post', 'post_title']