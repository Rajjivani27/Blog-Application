from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Comments

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    profile_pic = forms.ImageField()
    user_bio = forms.CharField()
    dob = forms.DateField()

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2','profile_pic','user_bio','dob']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    profile_pic = forms.ImageField()
    user_bio = forms.CharField()
    dob = forms.DateField()

    class Meta:
        model = CustomUser
        fields = ['username','email','profile_pic','user_bio','dob']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows':2,
                'placeholder':'Write a comment...'
            })
        }

