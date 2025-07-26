from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
from PIL import Image
from django.urls import reverse
from django.core.validators import FileExtensionValidator
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    profile_pic = models.ImageField(default='default.jpg')
    user_bio = models.CharField(max_length=50,default=' ')
    dob = models.DateField(default="2000-01-01")
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name="followers",
        through='Follows',
        through_fields=('follower','followed')
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)



class Posts(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser,related_name='liked_posts',blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
class PostMedia(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="media")
    files = models.FileField(
        upload_to="post_media/",
        null=True,
        blank=True,
        validators= [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','mp4','mov','webm'])]

    )
    
class Comments(models.Model):
    post = models.ForeignKey(Posts,related_name="post_comments",on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,related_name="user_comment",on_delete=models.CASCADE)
    content = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'comment done on {self.post} by {self.author}'

class Follows(models.Model):
    follower = models.ForeignKey(CustomUser,related_name="follower_relation",on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser,related_name="following_relation",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower','followed')

    def __str__(self):
        return f'{self.follower} follows {self.followed}'