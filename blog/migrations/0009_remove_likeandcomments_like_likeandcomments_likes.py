# Generated by Django 5.2.3 on 2025-06-30 17:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_likeandcomments_delete_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likeandcomments',
            name='like',
        ),
        migrations.AddField(
            model_name='likeandcomments',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
