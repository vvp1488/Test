from django.urls import path
from .views import RegistrationView,BaseView

urlpatterns = [
    path('', BaseView.as_view(),name='base'),
    path('register/',RegistrationView.as_view(),name='register')
]