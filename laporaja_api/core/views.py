from django.shortcuts import render
from django.http import HttpResponse
from .models import Report, User
from .serializers import ReportSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import generics
from rest_framework import mixins

# view to list 5 lastest reports
class ReportListView(generics.GenericAPIView, mixins.ListModelMixin):
    
    serializer_class = ReportSerializer
    queryset = Report.objects.all().order_by('-id')[:5]
    
    def get(self, request):
        return self.list(request)

