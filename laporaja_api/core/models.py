from django.db import models
import uuid
import os
import random

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('img', filename)


class User(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Report(models.Model):
    location_name = models.CharField(max_length=200)
    image = models.FileField(upload_to=get_file_path, default=None, blank=True, null=True)
    notes = models.CharField(max_length=1000, default=None, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=-6.200000)
    long = models.DecimalField(max_digits=9, decimal_places=6, default=106.816666)
    damage_severity = models.CharField(max_length=20, default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
