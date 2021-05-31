from django.conf.urls import url
from django.urls import path
from .views import ReportListView
urlpatterns = [
    path('home', ReportListView.as_view())
]
