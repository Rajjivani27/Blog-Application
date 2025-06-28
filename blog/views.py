from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegisterForm,UserUpdateForm,CommentForm
from django.contrib.auth.forms import UserCreationForm 
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import email_verification_token

#View for Registering new user
def register_page(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_verification_email(user,request)
            # username = form.cleaned_data.get('username')
            # messages.success(request,f'Account Created for {username}!')
            return redirect("/blog/verify-email-done/")
        else:
            print("Not Validating")
        
    else:
        form = UserRegisterForm()

    return render(request,'blog/register.html',{'form':form,'title':'Register'})

class PostListView(ListView):
    model = Posts
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html , ex:- blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Posts
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html , ex:- blog/post_list.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser,username = self.kwargs.get('username'))
        return Posts.objects.filter(author = user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser,username = self.kwargs.get('username'))
        context['user_profile'] = user
        return context


class PostDetailView(DetailView):
    model = Posts

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        post = self.object
        comments = Comments.objects.filter(post = post)
        context['comments'] = comments
        context['form'] = CommentForm
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.post = self.object
                comment.author = request.user
                comment.save()
                return redirect('post-detail',pk=self.object.pk)
        else:
            form = CommentForm()
        
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


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
    
class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comments

    success_url = "post-detail"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
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

def verify_email_done(request):
    return render(request,'blog/verify_email_done.html')

def verify_email_confirm(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user,token):
        user.is_active = True
        user.save()

        return render(request,'blog/verify_email_confirm.html')
    else:
        return HttpResponse("Invalid or expired verification link")




# Create your views here.
