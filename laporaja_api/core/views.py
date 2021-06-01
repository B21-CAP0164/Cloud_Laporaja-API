import re
from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework.views import APIView
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

# view for user history, reports detail and create report by user
class ReportUserView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    
    serializer_class = ReportSerializer
    
    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['user_id'])
        return user.report_set.all()
        
    
    def get(self, request, **kwargs):
        if 'id' in self.kwargs:
            try:
                report = Report.objects.get(id=self.kwargs.get('id'), user_id=self.kwargs.get('user_id'))
                serializer = ReportSerializer(report)
                return Response(serializer.data)
            except Report.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return self.list(request)


    def post(self, request, **kwargs):
        request.data['user'] = self.kwargs['user_id']
        return self.create(request, **kwargs)


# view to add user
class UserView(generics.GenericAPIView, mixins.CreateModelMixin):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self,request):
        return self.create(request)
