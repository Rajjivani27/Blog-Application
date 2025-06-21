from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm

def register_page(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST,request.FILES)

        if form.is_valid():
            print("Valid")
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}!')
            return redirect('/blog/home/')
        else:
            print("Not Validating")
        
    else:
        form = UserRegisterForm()

    return render(request,'blog/register.html',{'form':form,'title':'Register'})

def login_page(request):
    if request.method == "POST":
        data = request.POST

        email = data.get('email')
        password = data.get('password')

        user = CustomUser.objects.filter(email = email)
        if not user.exists():
            messages.error(request,'Invalid Email!!')
            return redirect('/blog/login/')
        else:
            user = authenticate(request,email = email,password=password)

            if user is None:
                messages.error(request,'Invalid Password!!')
                return redirect('/blog/login/')
            else:
                login(request,user)
                return redirect('/blog/home/')

    return render(request,'blog/login.html',{'title' : 'Login'})

@login_required(login_url='/blog/login/')
def home(request):
    posts = Posts.objects.all()
    context = {
        'posts' : posts,
        'title' : "Home"
    }
    return render(request,'blog/home.html',context)

@login_required(login_url='/blog/login/')
def about(request):
    return render(request,'blog/about.html',{'title':'About'})

@login_required(login_url='blog-login')
def profile(request):
    return render(request,'blog/profile.html',{'title' : 'Profile'})

def logoutView(request):
    logout(request)
    return redirect('/blog/login/')




# Create your views here.
