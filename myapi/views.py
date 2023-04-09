from django.shortcuts import render
from myapi.connect4 import *


# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import HeroSerializer
from .serializers import ColumnSerializer
from .models import Hero


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer
class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = ColumnSerializer
class MyAPIView(APIView):
    def get(self, request, column, format=None):
        print(column)
        data = connect4game(column)
        return Response(data)