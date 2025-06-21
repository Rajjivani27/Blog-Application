from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/',home,name="blog-home"),
    path('about/',about,name="blog-about"),
    path('login/',auth_views.LoginView.as_view(template_name = "blog/login.html"),name="blog-login"),
    path('register/',register_page,name="blog-register"),
    path('profile/',profile,name="blog-profile"),
    path('logout/',logoutView,name="blog-logout"),
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT) 