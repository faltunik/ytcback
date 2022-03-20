from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .models import Video, Comment
from .serializer import VideoSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    # def get_authvids(self):
    #     return Video.objects.filter(author=self.request.user)

    def create(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            # to do:
            # thumbnail manipulation
            # file rename to ytvid_<userid>_<timestamp>
            serializer.save()
            # let serializer.save(author=request.user), once we got user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        vids = get_object_or_404(Video, pk=pk)
        if vids.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        vids.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # to-do
    # How to update and how to include extra method
    # @action(detail=True)
    # def auth_videos(self, request):
    #     qeuryset = Video.objects.filter(author=request.user)
    #     serializer = VideoSerializer(qeuryset, many=True)
    #     return Response(serializer.data)

# @api_view(['GET'])
# def auth_videos(request):
#     qeuryset = Video.objects.filter(author=request.user)
#     serializer = VideoSerializer(qeuryset, many=True)
#     return Response(serializer.data)
