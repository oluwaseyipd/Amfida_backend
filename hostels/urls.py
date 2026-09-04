from django.urls import path
from .views import HostelListView, HostelDetailView, HostelCreateView, HostelUpdateView, HostelDeleteView, AreaListView, AreaCreateView, AreaUpdateView, AreaDeleteView

urlpatterns = [
    path('hostels/', HostelListView.as_view(), name='hostel-list'),
    path('hostels/create/', HostelCreateView.as_view(), name='create-hostel'),
    path('hostels/<int:pk>/', HostelDetailView.as_view(), name='hostel-detail'),
    path('hostels/<int:pk>/update/', HostelUpdateView.as_view(), name='update-hostel'),
    path('hostels/<int:pk>/delete/', HostelDeleteView.as_view(), name='delete-hostel'),
    path('areas/', AreaListView.as_view(), name='area-list'),
    path('areas/create/', AreaCreateView.as_view(), name='create-area'),
    path('areas/<int:pk>/update/', AreaUpdateView.as_view(), name='update-area'),
    path('areas/<int:pk>/delete/', AreaDeleteView.as_view(), name='delete-area')    
]