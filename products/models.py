import stripe
from django.conf import settings
from django.db import models

from products.managers import BasketQuerySet, PublishedManager

stripe.api_key = settings.STRIPE_SECRET_KEY


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
    stripe_product_price_id = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f"Продукт {self.name} | {self.category.name}"

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product["id"],
            unit_amount=round(self.price * 100),
            currency="rub"
        )
        return stripe_product_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price["id"]

        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | продукт {self.product.name}"

    def get_object_sum(self):
        return self.product.price * self.quantity

    def create_object_json(self):
        basket_json = {
            "product": self.product.name,
            "quantity": self.quantity,
            "price": float(self.product.price),
            "basket_object_sum": float(self.get_object_sum())
        }

        return basket_json
