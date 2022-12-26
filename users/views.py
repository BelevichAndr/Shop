from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from common.mixins import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification

User = get_user_model()


class UserLoginView(TitleMixin, LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    title = "Store - Авторизация"


class UserLogoutView(LogoutView):
    pass


class UserRegistrationView(TitleMixin, CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")
    title = "Store - Регистрация"


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile"))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        "title": "Store - Профиль",
        "form": form,
        "baskets": Basket.objects.filter(user=request.user),
    }
    return render(request, "users/profile.html", context=context)


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = "users/email_verification.html"
    title = "Store - Подтверждение электронной почты"

    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")
        email = kwargs.get("email")
        user = User.objects.get(email=email)
        email_verification = EmailVerification.objects.filter(code=code, user=user)

        if email_verification and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("index"))
