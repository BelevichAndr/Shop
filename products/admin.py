from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "category")
    fields = ("name", "description", "price", "quantity", "image", "category", "stripe_product_price_id",)
    search_fields = ("name", )


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ("product", "quantity")
