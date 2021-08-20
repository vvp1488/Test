from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveAPIView,
)
from .serializers import UserSerializer
from ..models import UserModel


class UserPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('Количество записей всего', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('Результат', data)

        ]))


class UserAPIView(ListAPIView,ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = UserPagination
    queryset = UserModel.objects.order_by('-id')


class UserDetailAPIView(RetrieveAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    lookup_field = 'id'





