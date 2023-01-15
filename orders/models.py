from django.conf import settings
from django.db import models

from products.models import Basket


class Order(models.Model):

    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3

    STATUSES = (
        (CREATED, "Created"),
        (PAID, "Paid"),
        (ON_WAY, "On way"),
        (DELIVERED, "Delivered"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    basket_history = models.JSONField(default=dict)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}. {self.first_name} {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.owner)
        self.status =  self.PAID
        self.basket_history = {
            "purchased_items": [basket.create_object_json() for basket in baskets],
            "total_sum": float(baskets.get_total_sum())
        }
        baskets.delete()
        self.save()
