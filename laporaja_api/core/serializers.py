from django.db.models import fields
from rest_framework import serializers
from .models import Report, User


class ReportListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Override `to_representation` method """
        repr = super().to_representation(instance)
        repr['user_id'] = str(repr['user_id'])  
        return repr

    class Meta:
        model = Report
        fields = ['id', 'image', 'location_name', 'user_id']

class ReportDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Override `to_representation` method """
        repr = super().to_representation(instance)
        repr['user_id'] = str(repr['user_id'])  
        return repr

    class Meta:
        model = Report
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """ Override `to_representation` method """
        repr = super().to_representation(instance)
        repr['user_id'] = str(repr['user_id'])  
        return repr

    class Meta:
        model = User
        fields = '__all__'