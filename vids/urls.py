from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('videolike', views.video_like, name='authorvids'),
    path('commentlike/<int:pk>', views.comment_like, name='authorvids'),
    path('videos', views.VideoView.as_view(), name='videos'),
    path('videos/<int:pk>', views.VideoDetail.as_view(), name='videodetail'),
    path('comment', views.CommentView.as_view(), name='comment'),
    path('comment/<int:pk>', views.CommentDetail.as_view(), name='commentdetail'),
    path('vidsearch', views.video_search, name='vidsearch'),
]