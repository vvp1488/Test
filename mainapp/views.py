from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from .forms import RegistrationForm
from django.contrib import messages
from .models import UserModel
from ipware import get_client_ip


class BaseView(View):

    def get(self,request,*args,**kwargs):
        ip = get_client_ip(request)
        user_current_ip = UserModel.objects.filter(ip_address=ip[0])
        users = UserModel.objects.all()
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
            messages.add_message(request, messages.INFO, 'Пользователь успешно создан')
            return HttpResponseRedirect('/')
        context = {
            'form' : form
        }
        return render(request,'registration.html', context)
