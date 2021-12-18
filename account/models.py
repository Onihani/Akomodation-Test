from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

# Create your models here.

class Manager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        if not(username):
            raise ValueError
        user = self.model(username=username, **kwargs)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    telephone = models.CharField(max_length=20, verbose_name='Telephone number')
#    USERNAME_FIELD = 'username'
    # id_number = models.CharField(max_length=20, verbose_name='Ghana card number')
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = 'users'
        permissions = (('update_user', 'can update info'),)
    def get_absolute_url(self):
        return reverse("info")
