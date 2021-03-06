from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to= 'videos/%Y/%m/%d', null=True, verbose_name="ytvid") # upload_to= 'videos/%Y/%m/%d' means, create a folder named videos inside BASE_DIR 
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True)
    like =  models.ManyToManyField(User, related_name='vidlike', blank=True)
    views = models.IntegerField(blank=True, default=0)
    # diff between blank and null
    # use of verbose and realted name

    def __str__(self):
        return self.title + ": " + str(self.date_uploaded)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.thumbnail:
            img = Image.open(self.thumbnail)
            if img.height > 300 or img.width > 500:
                output_size = (300, 600)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='parentchild')
    like =  models.ManyToManyField(User, related_name='comlike', blank=True)

    def __str__(self):
        return self.comment + ": " + str(self.date_posted)

    @property
    def is_parent(self):
        return True if self.parent is None else False

    @property
    def children(self):
        return Comment.objects.filter(parent=self)



# https://stackoverflow.com/questions/37737587/how-to-change-the-name-of-a-file-and-the-storage-location-on-upload-in-django
# 
