from django.urls import path

from orders.views import (CanselTemplateView, OrderDetailView, OrderCreateView,
                          OrderListView, SuccessTemplateView,
                          stripe_webhook_view)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="orders_list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("order-create/", OrderCreateView.as_view(), name="order_create"),
    path("order-success/", SuccessTemplateView.as_view(), name="order_success"),
    path("order-cansel/", CanselTemplateView.as_view(), name="order_cansel"),
    path("stripe/webhook/", stripe_webhook_view, name="stripe_webhook"),
]