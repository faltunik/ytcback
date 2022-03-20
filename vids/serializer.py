from rest_framework import serializers
from .models import Video, Comment

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'description', 'date_uploaded', 'author', 'video_file', 'thumbnail')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('video', 'comment', 'author', 'date_posted')