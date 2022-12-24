from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from common.mixins import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = "Store"


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    paginate_by = 3
    title = "Store - Каталог"
    extra_context = {
        "categories": ProductCategory.objects.all(),
    }

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        queryset = Product.published.filter(category_id=category_id) if category_id else Product.published.all()

        return queryset


@login_required
def add_basket(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    # return HttpResponseRedirect(request.META["HTTP_REFERER"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse("products:index")))


@login_required
def remove_basket(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
