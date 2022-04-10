from django.db import models


# Create your models here.
class newusers(models.Model):
    Name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=200)
    organization = models.CharField(max_length=500)
    purpose = models.CharField(max_length=500)
