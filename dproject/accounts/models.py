from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=64, null=True, blank=True)
    activation_expiry = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, default="user") 
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)


