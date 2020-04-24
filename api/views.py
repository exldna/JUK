from rest_framework import viewsets

from .serializers import HouseSerializer, CompanySerializer, NewsSerializer
from common.models import House, Company
from manager.models import News


class CompanyViewSet(viewsets.ModelViewSet):
	queryset = Company.objects.all()
	serializer_class = CompanySerializer


class HouseViewSet(viewsets.ModelViewSet):
	queryset = House.objects.all()
	serializer_class = HouseSerializer


class NewsViewSet(viewsets.ModelViewSet):
	queryset = News.objects.all()
	serializer_class = NewsSerializer


# Create your views here.
