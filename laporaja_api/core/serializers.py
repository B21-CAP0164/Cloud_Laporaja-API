from django.db.models import fields
from rest_framework import serializers
from .models import Report

class ReportListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['id', 'image', 'location_name', 'user_name']


class ReportDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Report
        fields = '__all__'
