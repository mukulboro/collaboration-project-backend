from django.db import models
import uuid
import os

class TimeStampMixIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ProfilePicture(TimeStampMixIn):
    def image_name(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return os.path.join('media/profile/', filename)
    
    image_path = models.ImageField(upload_to=image_name)

# Create your models here.
