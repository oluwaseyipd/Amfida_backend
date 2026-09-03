from django.contrib import admin

from .models import LandLord, Agent, OtpVerification

admin.site.register(LandLord)
admin.site.register(Agent)
admin.site.register(OtpVerification)
