from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.views import PasswordResetView,PasswordResetConfirmView


urlpatterns = [
    path('home/',PostListView.as_view(),name="blog-home"),
    path('follow/<int:user_id>/',follow_user,name="follow-user"),
    path('unfollow_user/<int:user_id>/',unfollow_user,name="unfollow_user"),
    path('user/<str:username>/',UserPostListView.as_view(),name="user-posts"),
    path('user/<str:username>/liked/',UserLikedPostView.as_view(),name="user-liked-posts"),
    path('user/<str:username>/commented_posts/',UserCommentedPostsView.as_view(),name="user-commented-posts"),
    path('about/',about,name="blog-about"),
    path('search/',search,name="search"),
    path('login/',auth_views.LoginView.as_view(template_name = "blog/login.html"),name="blog-login"),
    path('register/',register_page,name="blog-register"),
    path('verify-email-done/',verify_email_done,name="verify_email_done"),
    path('verify-email-confirm/<uidb64>/<token>/',verify_email_confirm,name="verify_email_confirm"),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete"),
    path('post/<int:pk>/like/',LikeToggleView.as_view(),name="toggle-like"),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(),name="comment-delete"),
    path('profile/',profile,name="blog-profile"),
    path('logout/confirm/',LogoutConfirmView.as_view(),name="logout-confirm"),
    path('logout/',LogOutView.as_view(),name="blog-logout"),
    path('post-list-api/',PostListAPI.as_view(),name="post_list_api"),
    path('post_create_api/',PostCreateAPI.as_view(),name="post-create-api"),
    path('post_delete_api/<int:pk>/',PostDetailAPI.as_view(),name="post-delete-api"),
    path('user_register_api/',CustomUserAPI.as_view(),name="user-register-api"),
    path('comment_list_api/',CommentListApi.as_view(),name="comment-list-api"),
    path('comments_of_post/<int:pk>/',SecificPostsCommentsAPI.as_view(),name="comments-on-post"),
    path('login_api/',LoginAPI.as_view(),name="login-api"),
    path('logout_api/',LogoutAPI.as_view(),name="logout-api"),
    path('password_reset_api/',CustomPasswordResetView.as_view(),name="password_reset_api"),
    path('reset_password_confirm/',PasswordResetConfirmView.as_view(),name="password-reset-confirm-api"),
    path('who_am_i_api/',WhoAmIAPI.as_view(),name="who-am-i-api"),
    path('api/token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT) 