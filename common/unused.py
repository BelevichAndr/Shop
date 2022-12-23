from django.contrib import auth, messages
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView

from products.models import Basket, Product, ProductCategory
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import User


def login(request):
    """ Функция обработчик для логина"""

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            # TODO
            print("ошибка")  # Сделать всплывающие сообещния
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "users/login.html", context=context)


def products(request, category_id=None, page_number=1):
    """Функция обработчик для списка товаров"""

    products = Product.published.filter(category_id=category_id) if category_id else Product.published.all()

    pruducts_on_page = 3
    paginator = Paginator(products, pruducts_on_page)
    try:
        products_paginator = paginator.page(page_number)
    except EmptyPage:
        products_paginator = paginator.page(1)

    context = {
        "title": "Store - Каталог",
        "products": products_paginator,
        "categories": ProductCategory.objects.all(),
    }
    return render(request, "products/products.html", context=context)


class UserProfileView(UpdateView):
    """Класс обработчик для профиля пользователя.
        Не получается реализовать как нужно"""
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title"] = "Store - Профиль"
        context["baskets"] = Basket.objects.filter(user=self.request.user)


def registration(request):
    """Функция обработчик для регистрации"""
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return HttpResponseRedirect(reverse("users:login"))
        else:
            print("ошибка")
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "users/register.html", context=context)
