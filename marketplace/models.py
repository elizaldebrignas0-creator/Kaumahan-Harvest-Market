from decimal import Decimal

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_approved", True)
        extra_fields.setdefault("user_type", "buyer")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("buyer", "Buyer"),
        ("seller", "Seller"),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    shipping_address = models.TextField(blank=True, null=True, help_text="Default shipping address for orders")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="buyer")
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_permit = models.FileField(
        upload_to="business_permits/", blank=True, null=True
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    is_approved = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.full_name or self.email

    @property
    def is_buyer(self) -> bool:
        return self.user_type == "buyer"

    @property
    def is_seller(self) -> bool:
        return self.user_type == "seller"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FRUITS', 'Fruits'),
        ('VEGETABLES', 'Vegetables'),
        ('GRAINS', 'Grains & Cereals'),
        ('TUBERS', 'Root Crops & Tubers'),
        ('HERBS', 'Herbs & Spices'),
        ('DAIRY', 'Dairy & Eggs'),
        ('MEAT', 'Meat & Poultry'),
        ('SEAFOOD', 'Seafood'),
        ('PROCESSED', 'Processed Foods'),
        ('BEVERAGES', 'Beverages'),
        ('ORGANIC', 'Organic Products'),
        ('OTHERS', 'Other Agricultural Products'),
    ]
    
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='FRUITS',
        help_text='Select the most appropriate category for your product'
    )
    
    UNIT_CHOICES = [
        ('KG', 'per kilogram (kg)'),
        ('G', 'per gram (g)'),
        ('PC', 'per piece'),
        ('SACK', 'per sack'),
        ('BUNCH', 'per bunch'),
        ('LITRE', 'per litre (L)'),
        ('ML', 'per millilitre (ml)'),
        ('DOZEN', 'per dozen'),
        ('PACK', 'per pack'),
        ('BOX', 'per box'),
    ]
    
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='KG',
        help_text='Select the unit of measurement for pricing'
    )
    
    image = models.ImageField(upload_to="static/products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    @property
    def average_rating(self) -> Decimal | None:
        agg = self.reviews.filter(is_approved=True).aggregate(models.Avg("rating"))
        return agg["rating__avg"]


class CartItem(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("buyer", "product")

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self) -> Decimal:
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_DELIVERED = "delivered"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_DELIVERED, "Delivered"),
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_made",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_received",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    payment_method = models.CharField(max_length=20, default="COD")
    shipping_address = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"

    @property
    def line_total(self) -> Decimal:
        return self.price * self.quantity


class Rating(models.Model):
    """Model to store product ratings"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings_given",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating} stars by {self.user.email} for {self.product.name}"


class RatingReview(models.Model):
    """Model to store product reviews with ratings"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_written",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating} stars by {self.buyer.email} for {self.product.name}"
