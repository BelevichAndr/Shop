from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from common.mixins import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from orders.services import create_stripe_checkout_session
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderCreateView(TitleMixin, CreateView):
    title = "Store - Order create"
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_create")
    
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = create_stripe_checkout_session(user=self.request.user, order_id=self.object.pk)

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context["baskets"] = Basket.objects.filter(user=self.request.user)
        return context


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = "orders/success.html"
    title = "Store - Order create - Success"


class CanselTemplateView(TitleMixin, TemplateView):
    template_name = "orders/cansel.html"
    title = "Store - Order create - Cansel"


class OrderListView(TitleMixin, ListView):
    template_name = "orders/orders.html"
    title = "Store - orders"
    context_object_name = "orders"
    ordering = ("-created_at")

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)


class OrderDetailView(DetailView):
    template_name = "orders/order.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context["title"] = f"Store - order #{self.object.pk}"
        return context



@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event["data"]["object"]["id"],
            expand=["line_items"],
        )
        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(pk=order_id)
    order.update_after_payment()
