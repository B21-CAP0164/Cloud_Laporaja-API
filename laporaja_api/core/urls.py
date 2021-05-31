from django.conf.urls import url
from django.urls import path
from .views import ReportListView, ReportUserView
urlpatterns = [
    path('report/', ReportListView.as_view()),
    url(r'^report/(?P<user_id>\d+)/$', ReportUserView.as_view()),
    # path('report/<int:fk>/<int:id>', ReportObjectView.as_view())
]
