from rest_framework import serializers

from mainapp.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=14)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    class Meta:
        model = UserModel
        fields = ('id','email', 'password', 'first_name', 'last_name', 'ip_address')
