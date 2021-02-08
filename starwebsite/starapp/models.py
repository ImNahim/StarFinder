from django.db import models
import os
from django.core.files.storage import FileSystemStorage

class Book(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Face(models.Model):
    face_Img = models.ImageField()

class Save(models.Model):
    your_face = models.ForeignKey(Face, related_name= "your", on_delete=models.CASCADE, null=True, blank=True)
    star_face = models.ForeignKey(Face, related_name= "star", on_delete=models.CASCADE, null=True, blank=True)
    merge_face = models.ForeignKey(Face, related_name= "merge", on_delete=models.CASCADE, null=True, blank=True)
    star_name = models.TextField(default='Nobody')