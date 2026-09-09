from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsListingAgentOwner
from .serializer import (
    ListingSerializer,
    ListingPhotoSerializer,
    ListingVideoSerializer,
    AmenitySerializer,
    ListingAmenitySerializer,
)
from .models import Listing, ListingPhoto, ListingVideo, Amenity, ListingAmenity


# 1. Listing List (Optimized with search, filtering, and ordering)
class ListingListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ListingSerializer
    queryset = (
        Listing.objects.select_related('agent', 'hostel', 'hostel__area', 'agent__user')
        .prefetch_related('images', 'videos', 'amenities')
        .all()
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'hostel': ['exact'],
        'hostel__area': ['exact'],
        'agent': ['exact'],
        'price': ['gte', 'lte', 'exact'],
    }
    search_fields = [
        'title',
        'description',
        'location',
        'hostel__name',
        'hostel__area__name',
        'amenities__name',
    ]
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']


# 2. Listing Detail
class ListingDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ListingSerializer
    queryset = (
        Listing.objects.select_related('agent', 'hostel', 'hostel__area', 'agent__user')
        .prefetch_related('images', 'videos', 'amenities')
        .all()
    )


# 3. Create Listing (Authenticated Agent only)
class CreateListingView(generics.CreateAPIView):
    permission_classes = [IsListingAgentOwner]
    serializer_class = ListingSerializer

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)


# 4. Update Listing (Authenticated Agent owner only)
class UpdateListingView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsListingAgentOwner]
    serializer_class = ListingSerializer
    queryset = (
        Listing.objects.select_related('agent', 'hostel', 'hostel__area', 'agent__user')
        .prefetch_related('images', 'videos', 'amenities')
        .all()
    )


# 5. Delete Listing (Authenticated Agent owner only)
class DeleteListingView(generics.DestroyAPIView):
    permission_classes = [IsListingAgentOwner]
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()


# 6. Listing Photo Upload & List
class ListingPhotoUploadView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsListingAgentOwner()]

    def get(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        photos = listing.images.all().order_by('sort_order', 'id')
        serializer = ListingPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        self.check_object_permissions(request, listing)

        serializer = ListingPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(listing=listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 7. Listing Photo Delete
class ListingPhotoDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        photo = get_object_or_404(ListingPhoto, pk=pk)
        # Verify ownership of the parent listing
        if not (request.user.is_staff or (hasattr(request.user, 'agent_profile') and photo.listing.agent == request.user.agent_profile)):
            return Response({'detail': 'You do not have permission to delete this photo.'}, status=status.HTTP_403_FORBIDDEN)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 8. Listing Video Create & List
class ListingVideoView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsListingAgentOwner()]

    def get(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        videos = listing.videos.all().order_by('sort_order', 'id')
        serializer = ListingVideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        self.check_object_permissions(request, listing)

        serializer = ListingVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(listing=listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 9. Listing Video Delete
class ListingVideoDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        video = get_object_or_404(ListingVideo, pk=pk)
        if not (request.user.is_staff or (hasattr(request.user, 'agent_profile') and video.listing.agent == request.user.agent_profile)):
            return Response({'detail': 'You do not have permission to delete this video.'}, status=status.HTTP_403_FORBIDDEN)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 10. Amenity List & Create
class AmenityListView(generics.ListCreateAPIView):
    queryset = Amenity.objects.all().order_by('name')
    serializer_class = AmenitySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
