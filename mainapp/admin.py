from django.contrib import admin
from .models import UserModel, User

admin.site.register(UserModel)
admin.site.register(User)