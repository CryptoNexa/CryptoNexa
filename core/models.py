import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        # Add custom exceptions for first_name, last_name, and date_joined
        if 'first_name' not in extra_fields:
            raise ValueError('You must provide a first name')
        if 'last_name' not in extra_fields:
            raise ValueError('You must provide a last name')

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    photo_id = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Quote(models.Model):
    currency_slug = models.SlugField()
    currency_symbol = models.CharField(max_length=50)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.currency_slug


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    num_market_pairs = models.IntegerField(null=True)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    total_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    max_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    infinite_supply = models.BooleanField(null=True)
    last_updated = models.DateTimeField(null=True)
    date_added = models.DateTimeField(null=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="My Watchlist")
    cryptocurrencies = models.ManyToManyField(Cryptocurrency, blank=True)

    def __str__(self):
        return f"{self.user}'s {self.name} Watchlist"

class FooterList(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    link = models.TextField(max_length=512, null=True, blank=True)
    def __str__(self):
        return f"{self.category} - {self.name} - {self.link}"
