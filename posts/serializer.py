from  rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'instagram_id', 'timestamp']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields  = '__all__'
        read_only_fields = ['id', 'instagram_id', 'timestamp', 'post']