"""
Используемые модули
"""
from django.db import models
from django.contrib.auth.models import User
from tenant.models import Company


class News(models.Model):
    """
    Модель БД для новостей
    """
    companyName = models.CharField(max_length=50)
    publicationDate = models.DateTimeField('date published')
    publicationTitle = models.CharField(max_length=50)
    publicationText = models.TextField(max_length=5000)


class Pass(models.Model):
    """
    Модель БД для пропусков
    """
    author = models.ForeignKey(to=User, on_delete=models.CASCADE())
    cr_date = models.DateTimeField(auto_now=True)
    status = models.TextField(max_length=7)
    target = models.TextField(max_length=6)
    name = models.TextField(null=True, blank=True, max_length=20)
    surname = models.TextField(null=True, blank=True, max_length=20)
    patronymic = models.TextField(null=True, blank=True, max_length=20)
    model = models.TextField(null=True, blank=True, max_length=20)
    color = models.TextField(null=True, blank=True, max_length=20)
    number = models.TextField(null=True, blank=True, max_length=20)
    aim = models.TextField(max_length=40)


