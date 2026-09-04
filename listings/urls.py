from django.urls import path
from .views import ListingListView, ListingDetailView, CreateListingView, UpdateListingView, DeleteListingView


urlpatterns = [
    path('listings/', ListingListView.as_view(), name='listing-list'),
    path('listings/create/', CreateListingView.as_view(), name='create-listing'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('listings/<int:pk>/update/', UpdateListingView.as_view(), name='update-listing'),
    path('listings/<int:pk>/delete/', DeleteListingView.as_view(), name='delete-listing'),
]