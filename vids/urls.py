from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('videolike/<int:pk>', views.video_like, name='authorvids'),
    path('videos', views.VideoView.as_view(), name='videos'),
    path('videos/<int:pk>', views.VideoDetail.as_view(), name='videodetail'),
]