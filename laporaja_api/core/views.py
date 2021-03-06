import base64
from django.core.files.base import ContentFile
from django.http.response import Http404, JsonResponse
from django.core.exceptions import *
from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework.views import APIView, exception_handler
from .models import Report
from .serializers import ReportListSerializer, ReportDetailSerializer
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
        return Report.objects.filter(google_id=self.kwargs.get('user_id'))
    
    def get(self, request, **kwargs):
        try: 
            return self.list(request)
        except Report.DoesNotExist:
            data = []
            return JsonResponse(data, safe=False)

class ReportDetailView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    
    serializer_class = ReportDetailSerializer
    lookup_field = "id"
    
    def get_queryset(self):
        return Report.objects.filter(id=self.kwargs.get('id'), google_id=self.kwargs.get('user_id'))
        
    
    def get(self, request, **kwargs):
        return self.retrieve(request)

class ReportPostView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    
    serializer_class = ReportDetailSerializer
    
    def get_queryset(self):
        return Report.objects.filter(google_id=self.kwargs.get('user_id'))
        

    def post(self, request, **kwargs):
        image_data = request.data['image']
        if request.data['image']:
            request.data['image'] = ContentFile(base64.b64decode(image_data), name='image.jpg')
            request.data['google_id'] = self.kwargs['user_id']
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'id': serializer.data.get('id')
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except BadRequest:
            return Response(
                {
                    'id': 0
                },
                status=status.HTTP_400_BAD_REQUEST
            )
