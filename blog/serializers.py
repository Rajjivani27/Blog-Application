from rest_framework import serializers
from .models import Posts

class PostsSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id','title','content','date_posted','author','likes_count','is_liked_by_user','profile_pic']
    
    def get_profile_pic(self,obj):
        request = self.context.get('request')
        author = obj.author
        if author.profile_pic:
            return request.build_absolute_uri(author.profile_pic.url)
        return None

    def get_author(self,obj):
        return obj.author.username
    
    def get_likes_count(self,obj):
        return obj.likes.count()
    
    def get_is_liked_by_user(self,obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['title','content']