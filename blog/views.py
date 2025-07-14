import requests
import google.generativeai as genai
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegisterForm,UserUpdateForm,CommentForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .utils import *
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import email_verification_token
from django.views import View
from BlogProject import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics,filters,status
from rest_framework.response import Response
from .serializers import PostsSerializer,PostCreateSerializer,CustomUserSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin,CreateModelMixin,RetrieveModelMixin,ListModelMixin
from rest_framework.authtoken.models import Token


#Configuring GEMINI SDK
genai.configure(api_key=settings.GOOGLE_API_KEY)

#Creating a Persistent model instance
model = genai.GenerativeModel('gemini-1.5-flash')

#for storing chat histroy(only for now)
chat_session = model.start_chat(history=[])

class PostListAPI(generics.ListCreateAPIView):
    """
    This is API view for PostLists
    """
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_posted','id']
    ordering = ['-date_posted']
    pagination_class = LimitOffsetPagination

    def list(self,request):
        context = {'request':request}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PostsSerializer(queryset,many=True,context=context)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}
    
class PostCreateAPI(generics.CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPI(RetrieveModelMixin,DestroyModelMixin,CreateModelMixin,generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,*kwargs)

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self,request,*args,**kwargs):
        obj = self.get_object()
        return self.destroy(request,*args,**kwargs)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CustomUserAPI(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        print("Request Data", request.data)

        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(request.data,status=status.HTTP_200_OK)
        else:
            print("Error",serializer.errors)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        return {'request':self.request}
    
class WhoAmIAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        response = Response(
                    {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    }
                )

        return response
    
class LoginAPI(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,username=email,password=password)

        if user is not None:
            token,_ = Token.objects.get_or_create(user=user)
            response = Response({'token':token.key},status=status.HTTP_200_OK)
            print(token,_)
            print(response)
            return response
        else:
            response = Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
            print(response)
            return response

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({"message":"Successfully Logged out"},status=status.HTTP_200_OK)


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
    
class UserLikedPostView(ListView):
    model = Posts
    template_name = 'blog/user_liked_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser,username = self.kwargs.get('username'))
        return user.liked_posts.all().order_by('-date_posted')
    
class UserCommentedPostsView(ListView):
    model = Posts
    template_name = 'blog/user_commented_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser,username = self.kwargs.get('username'))
        return Posts.objects.filter(post_comments__author = user).order_by('-date_posted')


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
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']

        abusive_words =  abuse_detector(title,content,chat_session)
        print(abusive_words)

        if abusive_words:
            highlighted_title = highlight_abusive_words(title,abusive_words)
            highlighted_content = highlight_abusive_words(content,abusive_words)

            form.add_error('title',mark_safe(f"Detected offensive words highighted above. Please remove them"))
            form.add_error('content',mark_safe(f"Detected offensive words highighted above. Please remove them"))

            self.highlighted_preview = {
                'title' : mark_safe(highlighted_title),
                'content': mark_safe(highlighted_content)
            }

            return self.form_invalid(form)
        

        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if hasattr(self,'highlighted_preview'):
            response.context_data['highlighted_preview'] = self.highlighted_preview
        return response
    
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

    def get_success_url(self):
        post = self.object.post
        return reverse('post-detail',kwargs={'pk':post.pk})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            print("Yes Authorized")
            return True
        
        print("No Not Authorized")
        return False
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        post = self.object.post
        context['post'] = post
        return context
    
class LikeToggleView(LoginRequiredMixin,View):
    def post(self,request,pk):
        post = get_object_or_404(Posts,pk=pk)
        print(post.id)

        liked = False
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked':liked,
            'like_count':post.total_likes()
        })



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


class LogoutConfirmView(TemplateView):
    template_name = 'blog/logout.html'

class LogOutView(LogoutView):
    http_method_names = ['post']
    next_page = 'blog-login'
            

def verify_email_done(request):
    return render(request,'blog/verify_email_done.html')

def verify_email_confirm(request,uidb64,token):
    try:
        print('I have reached Here')
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
