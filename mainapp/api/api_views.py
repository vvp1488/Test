from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from .serializers import (
    UserSerializer,
    RegistrationSerializer,
    UserListSerializer
)
from .renderers import UserJSONRenderer
from ..models import User
import jwt, datetime


def check_token(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Вы не вошли в систему!')
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Время токена(сеанса) в сети закончено.Пройдите авторизацию снова')
        return token

class RegisterAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPIView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(user)

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'token': token,
            "data": serializer.data
        }

        return response


class LogoutAPIView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : "Вы успешно вышли из системы!"
        }
        return response


# class UserPagination(PageNumberPagination):
#     page_size = 4
#     page_query_param = 'page'
#
#     def get_paginated_response(self, data):
#         return Response(OrderedDict([
#             ('Количество записей всего', self.page.paginator.count),
#             ('next', self.get_next_link()),
#             ('previous', self.get_previous_link()),
#             ('Результат', data)
#
#         ]))


class ListUserAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get(self,request, *args,**kwargs):
        check_token(self, request)
        return self.list(request, *args, **kwargs)


class UserAPIView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Вы не вошли в систему!')
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Время токена(сеанса) в сети закончено.Пройдите авторизацию снова')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDetailApiView(RetrieveUpdateAPIView,RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get(self,request,*args,**kwargs):
        check_token(self, request)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        check_token(self, request)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        check_token(self, request)
        return self.destroy(request, *args, **kwargs)

