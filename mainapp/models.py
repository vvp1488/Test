import jwt
from datetime import datetime, timedelta
from django.db import models, transaction
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserModel(models.Model):
    email = models.CharField(max_length=100, verbose_name='Електронная почта')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    ip_address = models.CharField(max_length=100, verbose_name='IP адрес пользователя', blank=True, null=True)

    def __str__(self):
        return self.email


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError('Поле email не может быть пустым')

        if extra_fields:
            first_name = extra_fields['first_name']
            last_name = extra_fields['last_name']


        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    #
    # def _create_user(self, email, password, **extra_fields):
    #     if not email:
    #         raise ValueError('Поле email не может быть пустым')
    #     try:
    #         with transaction.atomic():
    #             user = self.model(email=email, **extra_fields)
    #             user.set_password(password)
    #             user.save(using=self._db)
    #             return user
    #     except:
    #         raise
    #
    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)
    #
    # def create_superuser(self, email, password, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
