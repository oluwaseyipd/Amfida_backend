from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from .permissions import IsHostelOwner
from .models import Area, Hostel
from .serializer import AreaSerializer, HostelSerializer

# Create your views here.

# 1. Create Area
class AreaCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. List Areas
class AreaListView(APIView):
    def get(self, request):
        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 3. Update Area
class AreaUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        area = self.get_object(pk)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4. Delete Area
class AreaDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        area = self.get_object(pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 5. Create Hostel
class HostelCreateView(APIView):
    permission_classes = [IsHostelOwner]

    def post(self, request):
        serializer = HostelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(landlord=request.user.landlord_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HostelDetailView(APIView):
    def get_object(self, pk):
        try:
            return Hostel.objects.get(pk=pk)
        except Hostel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        hostel = self.get_object(pk)
        serializer = HostelSerializer(hostel)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
# 6. List Hostels
class HostelListView(APIView):
    def get(self, request):
        hostels = Hostel.objects.all()
        serializer = HostelSerializer(hostels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 7. Update Hostel  
class HostelUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsHostelOwner]
    queryset = Hostel.objects.all()

# 8. Delete Hostel
class HostelDeleteView(generics.DestroyAPIView):
    permission_classes = [IsHostelOwner]
    queryset = Hostel.objects.all()