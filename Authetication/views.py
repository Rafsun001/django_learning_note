from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from .models import Profile
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')
    full_name = request.data.get('full_name')

    if not email or not password or not role:
        return Response({"message": "All fields (role, password, email) are required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        existing_user = User.objects.get(username=email)
        if existing_user.is_active:
            return Response({"error": "This email is already registered and verified."}, status=400)
        else:
            existing_user.delete()
    except User.DoesNotExist:
        pass 

    user = User.objects.create_user(username=email, email=email, password=password)
    user.is_active = False
    user.save()

    profile = Profile.objects.create(user=user, role=role)
    otp = ''.join(random.choices(string.digits, k=6))
    profile.full_name = full_name
    profile.otp = otp
    profile.save()

    subject = 'Your OTP for Email Verification'
    message = f'Hello, your OTP to verify your email is: {otp}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({
        'message': 'Signup successful. Please verify OTP sent to your email.',
    }, status=status.HTTP_201_CREATED)
    
    
@api_view(['POST'])
def social_signup_signup(request):
    email = request.data.get('email')
    full_name = request.data.get('full_name')
    role = request.data.get('role')
    auth_provider = request.data.get('auth_provider')
    if not email or not full_name or not role or not auth_provider:
        return Response({'error': 'Please provide all the required fields'}, status=400)
    
    if User.objects.filter(username=email).exists():
        return Response({'error': 'User with this email already exists'}, status=400)

    user, created = User.objects.get_or_create(username=email, defaults={'email': email})
    profile, _ = Profile.objects.get_or_create(user=user)
    
    if created:
        profile.full_name = full_name
        profile.role = role
        profile.save()
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'message': 'Successfully authenticated.',
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'email': user.email,
            'profile_data': ProfileSerializer(profile).data,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({"message": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return Response({
        'refresh_token': str(refresh),
        'access_token': str(access_token),
        'profile_data': ProfileSerializer(user.profile).data,
        'message': 'Successfully authenticated.'
    },      status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def verify_otp(request):
    username = request.data.get('email')
    otp = request.data.get('otp')

    if not username or not otp:
        return Response({"Error": "Both Username and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if user_profile.otp == otp:
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        user_profile.save()
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(access_token),
            'profile_data': ProfileSerializer(user_profile).data,
            'message': 'OTP verified successfully and tokens issued.'
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            
@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    if request.method == 'GET':
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = ProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def resend_otp(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(username=email)
        profile = Profile.objects.get(user=user)
    except:
        return Response(
            {"Message": "Invalid Email."},
            status=status.HTTP_400_BAD_REQUEST
        )

    otp = ''.join(random.choices(string.digits, k=6))
    profile.otp = otp
    profile.save()
    subject = 'Your OTP for Email Verification'
    message = f'Hello, your OTP to verify your email is: {otp}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({
        'message': 'Please verify OTP sent to your email.',
    }, status=status.HTTP_201_CREATED)   

@csrf_exempt
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=email)
        profile = Profile.objects.get(user=user)
        otp = ''.join(random.choices(string.digits, k=6))
        profile.otp = otp
        profile.save()

        subject = 'Your Password Reset OTP'
        message = f'Hello, your OTP to reset your password is: {otp}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def verify_forgot_password_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    print(email, otp)
    if not email or not otp:
        return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=email)
        profile = Profile.objects.get(user=user)
        print(profile.otp)
        if profile.otp == otp:
            return Response({"message": "OTP is valid."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('password')

    if not email or not new_password:
        return Response({"error": "Email and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=email)
        profile = Profile.objects.get(user=user)

        if not profile.otp:
            return Response({"error": "Please verify OTP first."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        profile.otp = None
        profile.save()

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({"error": "Current and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)