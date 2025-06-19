from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=30,unique=True)
    profile_pic = models.ImageField()
    user_bio = models.CharField(max_length=50)
    dob = models.DateField(default="2000-01-01")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Posts(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
