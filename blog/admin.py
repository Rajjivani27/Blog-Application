from django.contrib import admin
from .models import *

class PostImageInline(admin.TabularInline):
    model = PostImages
    extra = 1

class PostsAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]

admin.site.register(CustomUser)
admin.site.register(Posts,PostsAdmin)
admin.site.register(PostImages)
admin.site.register(Comments)


# Register your models here.
