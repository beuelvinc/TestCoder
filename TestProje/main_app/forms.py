from xml.etree.ElementTree import QName
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from .models import *
from django.contrib.auth.hashers import make_password, check_password


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(required=False,initial=False,label='Is admin')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        if self.cleaned_data['is_admin']:
            user = User.objects.create_superuser(
                self.cleaned_data['username'],
                self.cleaned_data['email'],
                self.cleaned_data['password1']
            )
        else:
            user = User.objects.create_user(
                self.cleaned_data['username'],
                self.cleaned_data['email'],
                self.cleaned_data['password1']
            )
        return user

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', "password")

    def clean_password(self):
        data = self.cleaned_data['password']
        # encrypt stuff
        data=make_password(data)

        return data


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('picture',)



class ProductForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Product
 
        # specify fields to be used
        fields = [
            "name",
            "description"]



class ProductFormCreate(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Product
 
        # specify fields to be used
        fields = [
            "name",
            "description",'image_product','stores']