from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

def register_page(request):
    if request.method == "POST":
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phone_number')
        dob = data.get('dob')
        bio = data.get('bio')
        profile_pic = request.FILES.get('profile_pic')

        user1 = CustomUser.objects.filter(username = username)
        user2 = CustomUser.objects.filter(email = email)
        user3 = CustomUser.objects.filter(phone_number = phone_number)

        if user1.exists():
            messages.error(request,"Username already exist!! Please enter another username")
            return redirect('/blog/register/')
        
        elif user2.exists():
            messages.error(request,"Email already used by another User!!")
            return redirect('/blog/register/')
        
        elif user3.exists():
            messages.error(request,"Phone number already used by another User!!")
            return redirect('/blog/register/')


        user = CustomUser.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            phone_number = phone_number,
            dob = dob,
            user_bio = bio,
            profile_pic = profile_pic
        )

        user.set_password(password)
        user.save()

        messages.success(request,"Account Created Succesfully! Please Log in Now")


    return render(request,'blog/register.html',{'title' : 'Register'})

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

def logoutView(request):
    logout(request)
    return redirect('/blog/login/')




# Create your views here.
