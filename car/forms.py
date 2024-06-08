from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from .models import Comment

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment', )