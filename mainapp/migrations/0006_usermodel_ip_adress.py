# Generated by Django 3.2.6 on 2021-08-19 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210819_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='ip_adress',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='IP адрес пользователя'),
        ),
    ]