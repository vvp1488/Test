from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View

from .forms import RegistrationForm, LoginForm, TaskForm
from django.contrib import messages
from .models import User, Task
from ipware import get_client_ip



class BaseView(View):

    def get(self,request,*args,**kwargs):
        users =  User.objects.all()
        tasks = Task.objects.filter(user=request.user.id)

        context = {
            'users': users,
            'tasks': tasks
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
            User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"]
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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.add_message(request, messages.INFO, f'Успешно вошли в систему под {request.user}')
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)

class DeleteTask(View):

    def get(self, request, *args, **kwargs):
        task = Task.objects.filter(id=kwargs.get('id'))
        task.delete()
        messages.add_message(request, messages.SUCCESS, 'Задание выполнено!')
        return HttpResponseRedirect('/')

class AddTask(View):

    def get(self, request, *args, **kwargs):
        form = TaskForm(request.POST or None)
        # if form.is_valid():
        #     name = form.cleaned_data['name']
        #     description = form.cleaned_data['description']
        return render(request,'add_task.html',context={'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()
            user = request.user
            print(user)
            Task.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                user=request.user
            )
            messages.add_message(request, messages.INFO, 'Задание добавлено')
            return HttpResponseRedirect('/')
        return render(request, 'add_task.html', context={'form': form})


