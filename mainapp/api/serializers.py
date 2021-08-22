from django.core.validators import RegexValidator
from rest_framework import serializers

from mainapp.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100, validators=[
        RegexValidator(
            regex=r'(@gmail.com)$|(@icloud.com)$',
            message='Почта в доменах gmail.com и icloud.com не принимается!',
            code='invalid',
            inverse_match=True,
        )
    ])
    password = serializers.CharField(
        min_length=7,
        max_length=16, validators=[
            RegexValidator(
                regex=r'^[A-Z]\w*(?=\w*\d)(?=\w*[a-z])(?=\w*[_]).*$',
                message='Пароль должен состоять из буквенно-цифровых символов, подчеркивания, обязательно начинаться с прописной (заглавной) буквы',
                code='invalid',
                inverse_match=False,
            )
        ])
    first_name = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[a-zA-Z-]*[a-zA-Z-]$',
            message='Допустимо только буквы и тире',
            code='invalid',
            inverse_match=False,
        )
    ])
    last_name = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[a-zA-Z-\s]*[a-zA-Z-\s]$',
            message='Допустимо только буквы, тире и пробел.',
            code='invalid',
            inverse_match=False,
        )
    ])

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'first_name', 'last_name'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


