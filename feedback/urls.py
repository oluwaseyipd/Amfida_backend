from django.urls import path

from .views import ReportListView, ReportCreateView, ReportDeleteView, ReviewListView, ReviewCreateView, ReviewDeleteView

urlpatterns = [
    path('report/', ReportListView.as_view(), name='report-list'),
    path('report/create/', ReportCreateView.as_view(), name='create-report'),
    path('report/<int:pk>/delete/', ReportDeleteView.as_view(), name='delete-report'),
    path('review/', ReviewListView.as_view(), name='review-list'),
    path('review/create/', ReviewCreateView.as_view(), name='create-review'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete-review'),
]