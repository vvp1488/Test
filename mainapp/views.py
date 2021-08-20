from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from .models import UserModel
from ipware import get_client_ip


class BaseView(View):

    def get(self,request,*args,**kwargs):
        ip = get_client_ip(request)
        user_current_ip = UserModel.objects.filter(ip_address=ip[0])
        users = UserModel.objects.all()
        print(request.user.is_authenticated)
        print(request.user)
        context = {
            'user_current_ip': user_current_ip,
            'users': users,
        }
        return render(request, 'base.html', context)



class RegistrationView(View):

    def get(self,request,*args,**kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form' : form,
        }
        return render(request,'registration.html',context)

    def post(self,request,*args,**kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            ip, is_routable = get_client_ip(request)
            UserModel.objects.create(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                ip_address=ip
            )
            User.objects.create_user(
                username=f'{form.cleaned_data["email"]}',
                password=f'{form.cleaned_data["password"]}',
                first_name=f'{form.cleaned_data["first_name"]}',
                last_name=f'{form.cleaned_data["last_name"]}'
            )
            messages.add_message(request, messages.INFO, 'Пользователь успешно создан')
            return HttpResponseRedirect('/')
        context = {
            'form' : form
        }
        return render(request,'registration.html', context)


class LoginView(View):

    def get(self,request,*args,**kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.INFO, f'Успешно вошли в систему под {request.user}')
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)


