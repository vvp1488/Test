from django.urls import path
from .views import (
    RegistrationView,
    BaseView,
    LoginView,
    DeleteTask,
    AddTask
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', BaseView.as_view(),name='base'),
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('delete-task/<int:id>', DeleteTask.as_view(),name='delete_task'),
    path('add-task/', AddTask.as_view(), name='add_task')
]