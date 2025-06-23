from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegisterForm,UserUpdateForm
from django.contrib.auth.forms import UserCreationForm 
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

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

def home(request):
    posts = Posts.objects.all()
    context = {
        'posts' : posts,
        'title' : "Home"
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Posts
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html , ex:- blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Posts


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Posts
    fields = ['title','content']
    success_url = "/blog/home/"

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Posts
    fields = ['title','content']
    success_url = "/blog/home/"

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self): 
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
        
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Posts

    success_url = "/blog/home/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

@login_required(login_url='blog-login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request,'Your account has been updated successfully!')
            return redirect('blog-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form' : u_form,
        'title' : 'Profile'
    }
    return render(request,'blog/profile.html',context)

def logoutView(request):
    logout(request)
    return redirect('/blog/login/')




# Create your views here.
