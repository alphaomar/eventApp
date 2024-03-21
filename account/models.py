from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

# Create your models here.


class CustomUser(AbstractUser):
    USER = 'user'
    ORGANIZER = 'organizer'
    ADMIN = 'admin'

    ROLES_CHOICES = [
        (USER, 'user'),
        (ORGANIZER, 'organizer'),
        (ADMIN, 'admin'),
        ]

    username = None
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default=USER)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')),
                              blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=100, blank=True)
    subscription_status = models.BooleanField(default=False)

    email = models.EmailField(
        unique=True, blank=False, error_messages={"unique": "A user with that email already exists."}
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email





