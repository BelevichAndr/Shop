from django.conf import settings
from django.db import models

from products.managers import BasketQuerySet, PublishedManager


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)  # null = True?

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="products_images/%Y/%m/%d")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f"Продукт {self.name} | {self.category.name}"


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | продукт {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity
