from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=30,unique=True)
    profile_pic = models.ImageField()
    user_bio = models.CharField(max_length=50)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

class Posts(models.Model):
    heading = models.CharField(max_length=50)
