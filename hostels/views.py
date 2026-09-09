from rest_framework import status, permissions, generics, filters
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsHostelOwner
from .models import Area, Hostel
from .serializer import AreaSerializer, HostelSerializer


# 1. Create Area (Admin only)
class AreaCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AreaSerializer


# 2. List Areas (Public)
class AreaListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AreaSerializer
    queryset = Area.objects.all().order_by('name')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


# 3. Update Area (Admin only)
class AreaUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AreaSerializer
    queryset = Area.objects.all()


# 4. Delete Area (Admin only)
class AreaDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AreaSerializer
    queryset = Area.objects.all()


# 5. Create Hostel (Authenticated Landlord only)
class HostelCreateView(generics.CreateAPIView):
    permission_classes = [IsHostelOwner]
    serializer_class = HostelSerializer

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user.landlord_profile)


# 6. Detail Hostel (Public)
class HostelDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = HostelSerializer
    queryset = Hostel.objects.select_related('area', 'landlord', 'landlord__user').all()


# 7. List Hostels (Public, optimized with search & filter)
class HostelListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = HostelSerializer
    queryset = Hostel.objects.select_related('area', 'landlord', 'landlord__user').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['area', 'landlord']
    search_fields = ['name', 'location', 'description', 'area__name']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


# 8. Update Hostel (Authenticated Landlord owner only)
class HostelUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsHostelOwner]
    queryset = Hostel.objects.select_related('area', 'landlord', 'landlord__user').all()
    serializer_class = HostelSerializer


# 9. Delete Hostel (Authenticated Landlord owner only)
class HostelDeleteView(generics.DestroyAPIView):
    permission_classes = [IsHostelOwner]
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer