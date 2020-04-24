from rest_framework import serializers

from common.models import Company, House
from manager.models import News


class NewsSerializer(serializers.ModelSerializer):

	class Meta:
		model = News
		fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

	class Meta:
		model = Company
		fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):

	class Meta:
		model = House
		fields = '__all__'

