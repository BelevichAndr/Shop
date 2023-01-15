import stripe
from django.conf import settings
from django.urls import reverse

from products.models import Basket


def create_stripe_checkout_session(user, order_id):
    baskets = Basket.objects.filter(user=user)
    checkout_session = stripe.checkout.Session.create(
        line_items=baskets.get_stripe_products(),
        metadata={"order_id": order_id},
        mode="payment",
        success_url=settings.DOMAIN_NAME + reverse("orders:order_success"),
        cancel_url=settings.DOMAIN_NAME + reverse("orders:order_cansel"),
    )

    return checkout_session