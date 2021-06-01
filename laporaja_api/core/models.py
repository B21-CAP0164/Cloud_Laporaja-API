from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Report(models.Model):
    location_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img', default=None, blank=True, null=True)
    notes = models.CharField(max_length=1000, default=None, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=-6.200000)
    long = models.DecimalField(max_digits=9, decimal_places=6, default=106.816666)
    damage_type = models.CharField(max_length=100)
    damage_severity = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
