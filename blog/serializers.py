from rest_framework import serializers
from .models import Posts,CustomUser,Comments
from .utils import send_verification_email

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

class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,style={'input_type':'password'})
    class Meta:
        model = CustomUser
        fields = ['username','email','password','password2','user_bio','dob']
        extra_kwargs = {
            'password':{'write_only':True,'style':{'input_type':'password'}}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self,validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        validated_data['is_active'] = False
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        send_verification_email(user,self.context['request'])
        return user
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['post','autor','content']
