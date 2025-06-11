from django.db import models
# Create your models here.

class Posts(models.Model):
    heading = models.CharField(max_length=50)
