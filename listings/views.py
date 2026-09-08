from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsListingAgentOwner
from .serializer import ListingSerializer, ListingPhotoSerializer, ListingVideoSerializer, AmenitySerializer, ListingAmenitySerializer
from .models import Listing, ListingPhoto, ListingVideo, Amenity, ListingAmenity


class ListingListView(APIView):
    def get(self, request):
        queryset = Listing.objects.all()
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListingDetailView(APIView):
    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)


class CreateListingView(APIView):
    permission_classes = [IsListingAgentOwner]

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(agent=request.user.agent_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateListingView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsListingAgentOwner]

    def get_object(self):
        try:
            return Listing.objects.get(pk=self.kwargs['pk'])
        except Listing.DoesNotExist:
            raise Http404


class DeleteListingView(generics.DestroyAPIView):
    permission_classes = [IsListingAgentOwner]

    def get_object(self):
        try:
            return Listing.objects.get(pk=self.kwargs['pk'])
        except Listing.DoesNotExist:
            raise Http404
