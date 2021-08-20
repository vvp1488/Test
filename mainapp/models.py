from django.db import models



class UserModel(models.Model):

    email = models.CharField(max_length=100,verbose_name='Електронная почта')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    first_name = models.CharField(max_length=100,verbose_name='Имя')
    last_name = models.CharField(max_length=100,verbose_name='Фамилия')
    ip_address = models.CharField(max_length=100,verbose_name='IP адрес пользователя',blank=True,null=True)

    def __str__(self):
        return self.email