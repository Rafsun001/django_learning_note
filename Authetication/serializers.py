from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'email', 'full_name', 'image', 'role', 'otp', 'auth_provider')
