from django.urls import path

from products.views import ProductListView, add_basket, remove_basket

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("category/<int:category_id>", ProductListView.as_view(), name="category"),
    path("page/<int:page>", ProductListView.as_view(), name="products_page_number"),
    path("basket/add/int:<product_id>", add_basket, name="add_basket"),
    path("basket/remove/int:<basket_id>", remove_basket, name="remove_basket"),
]
