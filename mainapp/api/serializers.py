from rest_framework import serializers

from mainapp.models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id','email', 'password', 'first_name', 'last_name', 'ip_address')
