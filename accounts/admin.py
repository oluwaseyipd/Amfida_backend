from django.contrib import admin
from .models import User, LandLordProfile, AgentProfile, OtpVerification

admin.site.register(User)
admin.site.register(LandLordProfile)
admin.site.register(AgentProfile)
admin.site.register(OtpVerification)


