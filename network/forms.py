from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("caption", "image")
        widgets = {"caption": forms.Textarea(attrs={"rows": 3, "placeholder": "What's happening?"})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {"text": forms.TextInput(attrs={"placeholder": "Write a comment..."})}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "photo")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell people about yourself"})}
