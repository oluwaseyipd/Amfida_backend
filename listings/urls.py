from django.urls import path
from .views import (
    ListingListView,
    ListingDetailView,
    CreateListingView,
    UpdateListingView,
    DeleteListingView,
    ListingPhotoUploadView,
    ListingPhotoDeleteView,
    ListingVideoView,
    ListingVideoDeleteView,
    AmenityListView,
)

urlpatterns = [
    # Listings
    path('listings/', ListingListView.as_view(), name='listing-list'),
    path('listings/create/', CreateListingView.as_view(), name='create-listing'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('listings/<int:pk>/update/', UpdateListingView.as_view(), name='update-listing'),
    path('listings/<int:pk>/delete/', DeleteListingView.as_view(), name='delete-listing'),

    # Photos
    path('listings/<int:pk>/photos/', ListingPhotoUploadView.as_view(), name='listing-photos'),
    path('listing-photos/<int:pk>/', ListingPhotoDeleteView.as_view(), name='delete-listing-photo'),

    # Videos
    path('listings/<int:pk>/videos/', ListingVideoView.as_view(), name='listing-videos'),
    path('listing-videos/<int:pk>/', ListingVideoDeleteView.as_view(), name='delete-listing-video'),

    # Amenities
    path('amenities/', AmenityListView.as_view(), name='amenity-list'),
]