from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('home/',home,name="blog-home"),
    path('about/',about,name="blog-about"),
    path('login/',login_page,name="blog-login"),
    path('register/',register_page,name="blog-register"),
    path('logout/',logoutView,name="blog-logout")
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)