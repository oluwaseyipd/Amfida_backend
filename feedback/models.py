from django.db import models

from listings.models import Listing

class Review(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.listing}'


class Report(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    reason = models.TextField()
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report by {self.name} for {self.listing}'