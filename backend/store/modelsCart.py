from asyncio.windows_events import NULL
from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

from .modelsBook import Book


class Cart(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)


class CartItem(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    cart = models.OneToOneField(
        Cart, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    
    

    def __str__(self):
        return str(self.address)