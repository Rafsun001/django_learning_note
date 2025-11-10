from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'role', 'otp', 'auth_provider')
    search_fields = ('user', 'full_name', 'role', 'otp', 'auth_provider')