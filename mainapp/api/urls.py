from django.urls import path
from .api_views import UserAPIView, UserDetailAPIView

urlpatterns = [
    path('users/', UserAPIView.as_view(),name='users_list'),
    path('users/<int:id>/', UserDetailAPIView.as_view(),name='user'),
]