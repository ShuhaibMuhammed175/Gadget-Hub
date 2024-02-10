import datetime
import os
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models


def get_file_name(request, filename):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_file_name = '%s%s' % (current_time, filename)
    return os.path.join('uploads/', new_file_name)


def product_file_name(request, filename):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_file_name = '%s%s' % (current_time, filename)
    return os.path.join('uploads/', new_file_name)


class Category(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to=get_file_name, null=True, blank=True)
    desc = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=product_file_name, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    old_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, null=True, blank=True)
    new_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, null=True, blank=True)
    desc = models.TextField(max_length=800, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    STATUS_CHOICES = (
        ('cart', 'In Cart'),
        ('ordered', 'Ordered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')

    def total_price(self):
        return self.quantity * self.product.new_price


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s review on {self.product.name}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('order_placed', 'order_placed'),
        ('shipped', 'shipped'),
        ('out_for_delivery', 'out_for_delivery'),
        ('delivered', 'delivered')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='order_placed')

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return Decimal(self.quantity) * self.price
