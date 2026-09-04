from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
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
    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateListingView(APIView):
    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)

    def put(self, request, pk):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteListingView(APIView):
    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        listing = self.get_object(pk)
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)