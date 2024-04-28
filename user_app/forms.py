from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from user_app import models as user_app_models

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'my-input-reg'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'login', 'class': 'my-input-reg'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'my-input-reg'}))
    password2 = forms.CharField(label='Password(2)', widget=forms.PasswordInput(attrs={'placeholder': 'repeat password', 'class': 'my-input-reg'}),
                                help_text='Password must have digits [0-9], chars [A-Za-z] and special characters [?.,!@#$%^&*()\/|]',)

    class Meta:
        model = user_app_models.User
        fields = ('email', 'username', 'password1', 'password2')

class CustomUserDataChangeForm(UserChangeForm):
    image = forms.ImageField()
    description = forms.CharField()

    class Meta:
        model = user_app_models.User
        fields = ('image', 'description')

class CustomUserPasswordChangeForm(UserChangeForm):
    old_password = forms.CharField()
    new_password = forms.CharField()

class TagForm(forms.Form):
    tag_field = forms.CharField(max_length=128)

class UserLogin(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'my-input-reg'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'my-input-reg'}))

class UserDeleteForm(forms.Form):
    password1 = forms.CharField()
    password2 = forms.CharField()