from django import forms
from .models import User, Task
from django.core.validators import RegexValidator


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=100, validators=[
        RegexValidator(
            regex=r'(@gmail.com)$|(@icloud.com)$',
            message='Почта в доменах gmail.com и icloud.com не принимается!',
            code='invalid',
            inverse_match=True,
        )
    ])
    password = forms.CharField(min_length=7, max_length=16, validators=[
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(f'Пользователь с почтой {email} уже существует')
        return email

    def save(self):
        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=20)
    confirm_password = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Електронная почта'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        if not User.objects.filter(email=email):
            raise forms.ValidationError('Пользователя не найдено в системе')

        return self.cleaned_data

    def save(self):
        return self.cleaned_data


class TaskForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    #
    # class Meta:
    #     model = Task
    #     fields =['name', 'description','user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['description'].label = 'Описание'

    def save(self):
        return self.cleaned_data