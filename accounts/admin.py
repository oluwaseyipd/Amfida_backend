from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LandLordProfile, AgentProfile, OtpVerification


class LandLordProfileInline(admin.StackedInline):
    model = LandLordProfile
    can_delete = False
    verbose_name_plural = 'Landlord Profile'


class AgentProfileInline(admin.StackedInline):
    model = AgentProfile
    can_delete = False
    verbose_name_plural = 'Agent Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (LandLordProfileInline, AgentProfileInline)
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )


@admin.register(LandLordProfile)
class LandLordProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_status', 'verified_at')
    list_filter = ('verification_status',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_status', 'agency_approval', 'verified_at')
    list_filter = ('verification_status', 'agency_approval')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(OtpVerification)
class OtpVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('is_verified',)
    search_fields = ('email', 'phone_number')
