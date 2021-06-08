from django.conf.urls import url
from django.urls import path
from .views import ReportListView, ReportHistoryView, ReportDetailView, ReportPostView
urlpatterns = [
    path('report/', ReportListView.as_view()),
    url(r'^report/(?P<user_id>\d+)/$', ReportHistoryView.as_view()),
    url(r'^report/(?P<user_id>\d+)/add/$', ReportPostView.as_view()),
    url(r'^report/(?P<user_id>\d+)/(?P<id>\d+)/$', ReportDetailView.as_view()),
]
