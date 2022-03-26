from functools import partial
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .models import Video, Comment
from .serializer import VideoSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F
from rest_framework.views import APIView
# F helps to access models field value

# Create your views here.

class VideoView(APIView):


    def get(self,  request, format=None):
        # format = None meaning???
        video = Video.objects.all()
        serializer = VideoSerializer(video, many=True) # converting complex python data types to json
        return Response(serializer.data)

    def post(self, request, format=None):
        # how to access data sent here
        # in request, we have that data in json format
        # how to modify those data
        # how to check whther it is valid or not
        # how to save
        # how to send response
        serializer = VideoSerializer(data=request.data)
        # checking whether serializer is valid or not
        if serializer.is_valid():
            # modifying the data
            # <------------>
            # To-DO
            # thumbnail manipulation
            # file renaming
            # <------------>
            serializer.save()
            # author= request.user
            # sending the response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDetail(APIView):

    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        #video = self.get_object(pk=pk)
        video = get_object_or_404(Video, id=pk)
        serializer = VideoSerializer(video)
        print('Current Video Views is ', video.views)
        video.views = F('views') + 1
        video.save()
        print('Video views changes to ', video.views)
        return Response(serializer.data)

    def delete(self, pk, request):
        #video = self.get_object(pk)
        video = get_object_or_404(Video, id=pk)
        if request.user == video.author:
            video.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        #video = self.get_object(pk= request.data['id'])
        video = get_object_or_404(Video, id=pk)
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        #video = self.get_object(pk= request.data['id'])
        video = get_object_or_404(Video, id=pk)
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def video_like(request):
    # video = Video.object.filter(pk=pk)
    video = get_object_or_404(Video, id = request.GET.get('getid', 1) )
    res = ""
    print(video.like)
    print(type(video.like))

    if request.user in video.like:
        video.like.remove(request.user)
        res = "unliked"
    else:
        video.like.add(request.user)
        res = "liked"
    return Response({'message': f"post is{res}"}, status=status.HTTP_200_OK)


class CommentView(APIView):
    def get(self, request):
        video = get_object_or_404(Video, id=request.GET.get('id', 1) )
        comment = Comment.objects.filter(video = video, parent=None)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    def get(self, request,  pk):
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        if comment.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def comment_like(request, pk):
    print(request.data)
    # how pk is sent to this function
    comment = get_object_or_404(Comment, id = pk )
    res = ""
    if request.user in comment.like:
        comment.like.remove(request.user)
        res = "unliked"
    else:
        comment.like.add(request.user)
        res = "liked"
    return Response({'message': f"comment is{res}"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def video_search(request):
    print(request.data)
    query = request.GET.get('query', None)
    if query is not None:
        videos = Video.objects.filter(title__icontains=query)  # name__icontains helps use ot filter name that contains
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def reply_list(request):
    print(request.data)
    comment = get_object_or_404(Comment, id = request.GET.get('getid', 1) )
    reply = comment.children() # collecting it's children
    serializer = CommentSerializer(reply, many=True)
    return Response(serializer.data)

    

