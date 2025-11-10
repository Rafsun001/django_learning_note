from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from .models import Profile, GetInTouch
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_data(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    image_url = ""
    if profile.image and hasattr(profile.image, 'url'):
        image_url = request.build_absolute_uri(profile.image.url)

    return Response({
       "image": image_url
    }, status=status.HTTP_200_OK)