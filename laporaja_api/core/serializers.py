from django.db.models import fields
from rest_framework import serializers
from .models import Report, User


class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id','location_name', 'user_id']

class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'