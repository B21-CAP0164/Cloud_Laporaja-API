import base64
from django.core.files.base import ContentFile
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework.views import APIView
from .models import Report, User
from .serializers import ReportListSerializer, ReportDetailSerializer,  UserSerializer
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import generics
from rest_framework import mixins

# view to list 5 lastest reports
class ReportListView(generics.GenericAPIView, mixins.ListModelMixin):
    
    serializer_class = ReportListSerializer
    queryset = Report.objects.all().order_by('-id')[:5]
    
    def get(self, request):
        return self.list(request)

# view for user history, reports detail and create report by user
class ReportHistoryView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    
    serializer_class = ReportListSerializer
    
    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['user_id'])
        return user.report_set.all()
    
    def get(self, request, **kwargs):
        try: 
            return self.list(request)
        except User.DoesNotExist:
            data = []
            return JsonResponse(data, safe=False)
            


class ReportDetailView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    
    serializer_class = ReportDetailSerializer
    lookup_field = "id"
    
    def get_queryset(self):
        # report = Report.objects.get(id=self.kwargs.get('id'), user_id=self.kwargs.get('user_id'))
        return Report.objects.filter(id=self.kwargs.get('id'), user_id=self.kwargs.get('user_id'))
        
    
    def get(self, request, **kwargs):
        return self.retrieve(request)

class ReportPostView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    
    serializer_class = ReportDetailSerializer
    
    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['user_id'])
        return user.report_set.all()
        

    def post(self, request, **kwargs):
        image_data = request.data['image']
        request.data['image'] = ContentFile(base64.b64decode(image_data), name='image.jpg')
        request.data['user'] = self.kwargs['user_id']
        return self.create(request, **kwargs)


# view to add user
class UserView(generics.GenericAPIView, mixins.CreateModelMixin):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self,request):
        return self.create(request)
