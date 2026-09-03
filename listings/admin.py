from django.contrib import admin

from .models import Listing, ListingPhoto, ListingVideo, Amenity, ListingAmenity

admin.site.register(Listing)
admin.site.register(ListingPhoto)
admin.site.register(ListingVideo)
admin.site.register(Amenity)
admin.site.register(ListingAmenity)