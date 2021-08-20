from django import forms
from .models import UserModel
from django.core.validators import EmailValidator,RegexValidator
import re


class RegistrationForm(forms.Form):

    email = forms.EmailField(max_length=100,validators=[
        RegexValidator(
            regex=r'(@gmail.com)$|(@icloud.com)$',
            message='Почта в доменах gmail.com и icloud.com не принимается!',
            code='invalid',
            inverse_match=True,
        )
    ])
    password = forms.CharField(min_length=7,max_length=16,validators=[
        RegexValidator(
            regex=r'^[A-Z]\w*(?=\w*\d)(?=\w*[a-z])(?=\w*[_]).*$',
            message='Пароль должен состоять из буквенно-цифровых символов, подчеркивания, обязательно начинаться с прописной (заглавной) буквы',
            code='invalid',
            inverse_match=False,
        )
    ])
    first_name = forms.CharField(validators=[
        RegexValidator(
            regex=r'^[a-zA-Z-]*[a-zA-Z-]$',
            message='Допустимо только буквы и тире',
            code='invalid',
            inverse_match=False,
        )
    ])
    last_name = forms.CharField(validators=[
        RegexValidator(
            regex=r'^[a-zA-Z-\s]*[a-zA-Z-\s]$',
            message='Допустимо только буквы, тире и пробел.',
            code='invalid',
            inverse_match=False,
        )
    ])

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email):
            raise forms.ValidationError(f'Пользователь с почтой {email} уже существует')
        return email

    def save(self):
        # new_user = UserModel.objects.create(
        #     email=self.cleaned_data['email'],
        #     password=self.cleaned_data['password'],
        #     first_name=self.cleaned_data['first_name'],
        #     last_name=self.cleaned_data['last_name']
        # )
        # return new_user
        return self.cleaned_data
