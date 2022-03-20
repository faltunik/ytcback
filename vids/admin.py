from django.contrib import admin
from .models import Video, Comment

# Register your models here.
@admin.register(Video)
class CustomVideoAdmin(admin.ModelAdmin):
  list_display = ['title', 'author', 'date_uploaded' ]

@admin.register(Comment)
class CustomCommentAdmin(admin.ModelAdmin):
  list_display = ['comment', 'author', 'date_posted' ]

