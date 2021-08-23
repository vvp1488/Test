from django.urls import path
from .api_views import (
    UserAPIView,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ListUserAPIView,
    UserDetailApiView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('users/', ListUserAPIView.as_view()),
    path('user/<int:id>', UserDetailApiView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
