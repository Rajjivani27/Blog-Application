from django.shortcuts import render
from .models import Posts

def home(request):
    posts = Posts.objects.all()
    context = {
        'posts' : posts,
        'title' : "Home"
    }
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

def register(request):
    return render(request,'blog/register.html',{'title' : 'Register'})

# Create your views here.
