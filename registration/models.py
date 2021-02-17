from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class Account(AbstractUser):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True)
    phone_number = models.CharField(default=None, null=True, blank=True, max_length=20, )
    avatar = models.ImageField(default='/users/user.jpg', upload_to='users')
    birthday = models.DateField(default=timezone.now())

    city = models.CharField(default=None, null=True, blank=True, max_length=255)
    work = models.CharField(default=None, null=True, blank=True, max_length=255)
    study = models.CharField(default=None, null=True, blank=True, max_length=255)
    current_info = models.CharField(default=None, null=True, blank=True, max_length=500)

    time_join = models.DateTimeField(default=timezone.now())

    banned = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_superuser = models.BooleanField(
        default=False,
    )

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def __str__(self):
        return self.username
