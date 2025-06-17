from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('home/',home,name="blog-home"),
    path('about/',about,name="blog-about"),
    path('register/',register,name="blog-register")
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)