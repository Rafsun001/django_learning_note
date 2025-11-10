from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    role = models.CharField(max_length=20, choices=role)
    otp = models.CharField(max_length=6, null=True, blank=True)
    auth_provider = models.CharField(max_length=20, default="email_password")
    
    def __str__(self):
        return f"{self.full_name} - {self.role}" 