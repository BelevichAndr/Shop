from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class ProductListViewTestCase(TestCase):

    fixtures = ["categories.json", "product.json"]

    def test_list(self):
        path = reverse("products:index")
        response = self.client.get(path)

        self._common_tests(response)
        posts_per_page = self._get_posts_per_page_number(response)

        self.assertEqual(list(response.context_data["object_list"]),
                         list(Product.published.all()[:posts_per_page]))

    def test_list_category(self):
        category = ProductCategory.objects.first()
        path = reverse("products:category", kwargs={"category_id": category.pk})
        response = self.client.get(path)

        self._common_tests(response)
        posts_per_page = self._get_posts_per_page_number(response)

        self.assertEqual(
            list(response.context_data["object_list"]),
            list(Product.published.filter(category=category.pk)[:posts_per_page]))

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data["title"], "Store - Каталог")
        self.assertTemplateUsed(response, "products/products.html")

    def _get_posts_per_page_number(self, response) -> int:
        posts_per_page = response.context_data["paginator"].per_page
        self.assertEqual(posts_per_page, 3)
        return posts_per_page
