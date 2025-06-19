from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField()
    profile_pic = forms.ImageField()
    user_bio = forms.CharField()
    dob = forms.DateField()

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2','phone_number','profile_pic','user_bio','dob']