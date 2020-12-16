from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .apps import ServiceConfig as pwu
#from Modules import PhotoWakeUp

# Create your models here.

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class Post(models.Model):
    name = models.CharField(null=False,blank=False,max_length=20)
    dir = models.TextField(null=False,blank=False,max_length=255)
    image = models.ImageField(upload_to="",blank=False,null=False,storage=OverwriteStorage())


    def __str__(self):
        return self.name

# class PhotoWakeUp(models.Model):
#     pwu = PhotoWakeUp()