from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'houses', views.HouseViewSet)
router.register(r'news', views.NewsViewSet)


urlpatterns = [
	path('', include(router.urls))
]