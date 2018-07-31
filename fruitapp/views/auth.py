import django,os,sys
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()
from fruitapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.shortcuts import render_to_response
from django.views import View
from django.views.generic import ListView, DetailView ,CreateView, UpdateView,DeleteView
from django.contrib import messages


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name '})
    )
    last_name = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name '})
    )

    username = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'})
    )
    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'First Name '})
    )
    email = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )






class SignUpView(View):
    def get(self,request):
        form = SignUpForm()
        return render(request,template_name='SignUpForm.html',context={'form':form,'title':'Signup | Online App'})

    def post(self,request):
        form =SignUpForm(request.POST)
        instance=dict()
        instance['first_name'] = form.data['first_name']
        instance['last_name'] = form.data['last_name']
        instance['username'] = form.data['username']
        instance['password'] = form.data['password']
        instance1=dict()
        instance1['email']=form.data['email']

        if form.is_valid():
            user = User.objects.create_user(**instance)
            instance1['user']=user
            userinfo = User_info(**instance1)
            userinfo.save()
            user=authenticate(
            request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request,user)
                return redirect('fruitapp:products')
            else:
                messages.error(request,'Invalid Credentials')

        return render(redirect,template_name='SignUpForm.html',context={'form':form,'title':'Signup | Online App'})






class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'})
    )

    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'First Name '})
    )




class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,template_name='LoginForm.html',context={'form':form,'title':'Signup | Online App'})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('fruitapp:products')
            else:
                messages.error(request, 'Invalid Credentials')

        return render(request,template_name='products.html')

def logout_user(request):
    logout(request)
    return redirect('fruitapp:login')
