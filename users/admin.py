from django.contrib import admin
from django.contrib.auth import get_user_model

from products.admin import BasketAdmin
from users.models import EmailVerification

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", )
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "expiration")
    fields = ("code, user, expiration", "created")
    readonly_fields = ("created_at",)
