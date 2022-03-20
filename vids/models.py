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

    def __str__(self):
        return self.title + ": " + str(self.date_uploaded)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image)
            if img.height > 300 or img.width > 500:
                output_size = (300, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment + ": " + str(self.date_posted)



# https://stackoverflow.com/questions/37737587/how-to-change-the-name-of-a-file-and-the-storage-location-on-upload-in-django
# 
